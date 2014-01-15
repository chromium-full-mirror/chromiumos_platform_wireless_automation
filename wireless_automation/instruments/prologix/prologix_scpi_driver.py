# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The driver for the Prologix internet CAT5 cable to GPIB cable converter
"""

import os
import select
import socket
import traceback

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging


class PrologixScpiDriver(object):
    """Wrapper for a Prologix TCP<->GPIB bridge.
    http://prologix.biz/gpib-ethernet-controller.html
    http://prologix.biz/index.php?dispatch=attachments.getfile&attachment_id=1

    Communication is over a plain TCP stream on port 1234.  Commands to
    the bridge are in-band, prefixed with ++.

    Notable instance variables include:

      self.auto: When 1, the bridge automatically addresses the target
        in listen mode.  When 0, we must issue a ++read after every
        query.  As of Aug '11, something between us and the Agilent 8960
        is wrong such that running in auto=0 mode leaves us hanging if
        we issue '*RST;*OPC?'
    """
    all_open_connections = {}

  #pylint:disable=too-many-arguments
    def __init__(self, hostname=None, port=1234, gpib_address=14,
                 read_timeout_seconds=30, connect_timeout_seconds=5):

        """Constructs a wrapper for the Prologix TCP<->GPIB bridge :
        Arguments:
            hostname: hostname of prologix device
            port: port number
            gpib_address: initial GPIB device to connect to
            read_timeout_seconds: the read time out for the socket to the
                prologix box
            connect_timeout_seconds: the read time out for the socket to the
                prologix box
        """
        logger_name = 'prologix'
        host_addr = 'IP:%s GPIB:%s: ' % (hostname, gpib_address)
        formatter_string = '%(asctime)s %(filename)s %(lineno)d ' + \
                           host_addr + '- %(message)s'
        self.scpi_logger = wireless_automation_logging.setup_logging(
            logger_name, formatter_string, level='INFO')

        self.scpi_logger.debug("Connecting to %s : %s ..." % (hostname, port))

        if hostname is None:
            raise wireless_automation_error.BadState(
                'PrologixScpiDriver needs a hostname')

        caller = self._get_caller()
        caller[0] = os.path.basename(caller[0])
        self.scpi_logger.debug('New Prologix driver called by :' + str(caller))

        self.connection_key = "%s:%s" % (hostname, port)
        self.connection_data = {self.connection_key: traceback.format_stack()}
        if self.connection_key in self.all_open_connections.keys():
            raise wireless_automation_error.BadState(
                'IP network connection to '
                'prologix is already in use. : %s ', self.all_open_connections)
        self.all_open_connections[self.connection_key] = self.connection_data
        self.read_timeout_seconds = read_timeout_seconds

        self.socket = self._get_socket_to_port(hostname, port,
                                               connect_timeout_seconds)
        self.auto = None
        self._set_auto(1)
        self._add_returns_to_responses()
        self._set_gpib_address(gpib_address)
        self.scpi_logger.debug('set read_timeout_seconds: %s ' %
                               self.read_timeout_seconds)
    #pylint:enable=too-many-arguments

    @classmethod
    def _get_socket_to_port(cls, hostname, port, connect_timeout_seconds):
        """
        @param hostname: Name of the host, e.g. 192.168.1.10
        @param port: Port number: 1234
        @param connect_timeout_seconds:  seconds to timeout
        @return: a socket object
        """
        sock = socket.socket()
        sock.settimeout(connect_timeout_seconds)
        try:
            sock.connect((hostname, port))
        except socket.error as msg:
            raise wireless_automation_error.SocketTimeout(msg)
        sock.setblocking(0)
        return sock

    def _get_caller(self):
        """
        Get the stack frame as list of strings. Used for
        printing debug log messages.
        @return: None
        """
        return list(self.scpi_logger.findCaller())

    def __del__(self):
        self.close()

    def _add_returns_to_responses(self):
        """
        Have the prologix box add a line feed to each response.
        Some instruments may need this.
        """
        self.send('++eot_enable 1')
        self.send('++eot_char 10')

    def _set_auto(self, auto):
        """Controls Prologix read-after-write (aka 'auto') mode."""
        # Must be an int so we can send it as an arg to ++auto.
        self.auto = int(auto)
        self.send('++auto %d' % self.auto)

    def close(self):
        """Closes the socket."""
        caller = list(self.scpi_logger.findCaller())
        caller[0] = os.path.basename(caller[0])
        self.scpi_logger.info('Close called by :' + str(caller))
        try:
            self.scpi_logger.error('Closing prologix devices at : %s ' %
                                   self.connection_key)
            self.all_open_connections.pop(self.connection_key)
        except KeyError:
            self.scpi_logger.error('Closed %s more then once' %
                                   self.connection_key)
        try:
            self.socket.close()
        except AttributeError:  # Maybe we close before we finish building.
            pass

    def _set_gpib_address(self, gpib_address):
        """
        Sets the GPIB address to talk to on the GPIB bus. This is used
        to select which instrument on the GPIB bus to use.
        @param gpib_address:
        @return:
        """
        for _ in range(10):
            self.send('++addr %s' % gpib_address)
            read_back_value = self._direct_query('++addr')
            try:
                if int(read_back_value) == int(gpib_address):
                    break
            except ValueError:
                # If we read a string, don't raise, just try again.
                pass
            self.scpi_logger.error('Set gpib addr to: %s, read back: %s' %
                                   (gpib_address, read_back_value))
            self.scpi_logger.error('Setting the GPIB address failed. ' +
                                   'Trying again...')

    def send(self, command, write_to_log=True):
        """
        @param command: The command to send
        @param write_to_log:  Write this message out to the log
        """
        if write_to_log:
            self.scpi_logger.info('] %s', command)
        try:
            self.socket.send(command + '\n')
        except Exception as exc:
            self.scpi_logger.error('sending SCPI command %s failed. ' %
                                   command)
            self.scpi_logger.exception(exc)
            raise SystemError('Sending SCPI command failed. '
                              'Did the instrument stopped talking?')

    def read(self, write_to_log=True):
        """Read a response from the bridge."""
        try:
            ready = select.select([self.socket], [], [],
                                  self.read_timeout_seconds)
        except Exception as exc:
            self.scpi_logger.exception(exc)
            msg = 'Read from the instrument failed. Timeout:%s' % \
                self.read_timeout_seconds
            self.scpi_logger.error(msg)
            raise SystemError(msg)

        if ready[0]:
            response = self.socket.recv(4096)
            response = response.rstrip()
            if write_to_log:
                self.scpi_logger.info('[ %s', response)
            return response

        self.close()
        msg = 'Connection to the prologix adapter worked.' \
            'But there was not data to read from the instrument.' \
            'Does that command return a result?' \
            'Bad GPIB port number, or timeout too short?'
        raise wireless_automation_error.InstrumentTimeout(msg)

    def query(self, command, write_to_log=True):
        """Send a GPIB command and return the response."""
        #self.SetAuto(1) #maybe useful?

        caller = list(self.scpi_logger.findCaller())
        caller[0] = os.path.basename(caller[0])
        self.scpi_logger.debug('Query called by :' + str(caller))

        self.send(command, write_to_log=write_to_log)
        if not self.auto:
            self.send('++read eoi')
        output = self.read(write_to_log=write_to_log)
        #self.SetAuto(0) #maybe useful?
        return output

    def _direct_query(self, command):
        """Sends a query to the prologix (do not send ++read).

        Returns: response of the query.
        """
        self.send(command)
        return self.read()

    def send_list(self, commands):
        """
        Sends a list of commands and verifies that they complete correctly.
        """
        assert isinstance(commands, list)
        for cmd in commands:
            self.send(cmd)
            self.retrieve_errors()

    def retrieve_errors(self):
        """Retrieves all SYSTem:ERRor messages from the device."""
        self.query('*OPC?', write_to_log=False)
        errors = []
        while True:
            error = self.query('SYSTem:ERRor?', write_to_log=False)
            if '+0,"No error"' in error:
                # We've reached the end of the error stack
                break

            if '-420' in error and 'Query UNTERMINATED' in error:
                # The GPIB bridge asked for a response when
                # the device didn't have one to give.
                self.scpi_logger.error(error)
                continue

            if '+292' in error and 'Data arrived on unknown SAPI' in error:
                # This may be benign; It is known to occur when we do a switch
                # from GPRS to WCDMA
                continue

            errors.append(error)

        self.send('*CLS', write_to_log=False)  # Clear status
        errors.reverse()
        if len(errors) > 0:
            self.scpi_logger.error(errors)
        return errors

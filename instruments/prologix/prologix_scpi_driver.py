# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os
import select
import socket
import traceback

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging


class PrologixScpiDriver:
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

    def __init__(self, hostname, port=1234, gpib_address=14,
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
        s = 'IP:%s GPIB:%s: ' % (hostname, gpib_address)
        formatter_string = '%(asctime)s %(filename)s %(lineno)d ' + s + \
                           '- %(message)s'
        self.scpi_logger = wireless_automation_logging.setup_logging(
            logger_name, formatter_string, level='INFO')

        caller = list(self.scpi_logger.findCaller())
        caller[0] = os.path.basename(caller[0])
        self.scpi_logger.debug('New Prologix driver called by :' + str(caller))

        self.connection_key = "%s:%s" % (hostname, port)
        self.connection_data = {self.connection_key: traceback.format_stack()}
        if self.connection_key in self.all_open_connections.keys():
            raise wireless_automation_error.BadState(
              'IP network connection to '
              'prologix is already in use. : %s ' % self.all_open_connections)
        self.all_open_connections[self.connection_key] = self.connection_data
        self.socket = connect_to_port(hostname, port, connect_timeout_seconds)
        self.read_timeout_seconds = read_timeout_seconds
        self.socket.setblocking(0)
        self.set_auto(1)
        self._add_carriage_returns_to_responses()
        self.set_gpib_address(gpib_address)
        self.scpi_logger.debug('set read_timeout_seconds: %s ' %
                               self.read_timeout_seconds)

    def __del__(self):
        self.close()

    def _add_carriage_returns_to_responses(self):
        """
        Have the prologix box add a line feed to each response.
        Some instruments may need this.
        """
        self.send('++eot_enable 1')
        self.send('++eot_char 10')

    def set_auto(self, auto):
        """Controls Prologix read-after-write (aka 'auto') mode."""
        # Must be an int so we can send it as an arg to ++auto.
        self.auto = int(auto)
        self.send('++auto %d' % self.auto)

    def close(self):
        """Closes the socket."""
        s = list(self.scpi_logger.findCaller())
        s[0] = os.path.basename(s[0])
        self.scpi_logger.info('Close called by :' + str(s))
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

    def set_gpib_address(self, gpib_address):
        max_tries = 10
        while max_tries > 0:
            max_tries -= 1
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
        if write_to_log:
            self.scpi_logger.info('] %s', command)
        try:
            self.socket.send(command + '\n')
        except Exception as e:
            self.scpi_logger.error('sending SCPI command %s failed. ' %
                                   command)
            self.scpi_logger.exception(e)
            raise SystemError('Sending SCPI command failed. '
                              'Did the instrument stopped talking?')

    def read(self, write_to_log=True):
        """Read a response from the bridge."""
        try:
            ready = select.select([self.socket], [], [],
                                  self.read_timeout_seconds)
        except Exception as e:
            self.scpi_logger.exception(e)
            s = 'Read from the instrument failed. Timeout:%s' % \
                self.read_timeout_seconds
            self.scpi_logger.error(s)
            raise SystemError(s)

        if ready[0]:
            response = self.socket.recv(4096)
            response = response.rstrip()
            if write_to_log:
                self.scpi_logger.info('[ %s', response)
            return response

        self.close()
        s = 'Connection to the prologix adapter worked.' \
            'But there was not data to read from the instrument.' \
            'Does that command return a result?' \
            'Bad GPIB port number, or timeout too short?'
        raise wireless_automation_error.InstrumentTimeout(s)

    def query(self, command, write_to_log=True):
        """Send a GPIB command and return the response."""
        #self.SetAuto(1) #maybe useful?

        s = list(self.scpi_logger.findCaller())
        s[0] = os.path.basename(s[0])
        self.scpi_logger.debug('Query called by :' + str(s))

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
                # This is benign; the GPIB bridge asked for a response when
                # the device didn't have one to give.
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

def connect_to_port(hostname, port, connect_timeout_seconds):
    # Right out of the python documentation,
    #  http://docs.python.org/library/socket.html
    for res in socket.getaddrinfo(
            hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, _, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            raise wireless_automation_error.SocketTimeout(
                'Failed to make a new socket object. ' + str(msg))
        try:
            s.settimeout(connect_timeout_seconds)
            s.connect(sa)
        except socket.error as msg:
            try:
                s.close()
            except Exception:
                pass  # Try to close it, but it may not have been created.
            temp_string_var = ' Could be bad IP address. Tried: %s : %s' % \
                              (hostname, port)
            raise wireless_automation_error.SocketTimeout(str(msg) +
                                                      temp_string_var)
    return s

#!/usr/bin/python
# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import copy
import mock
import unittest

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.instruments.prologix import prologix_scpi_driver
from hardware_setup import scpi_instruments
log = wireless_automation_logging.setup_logging('scpi_test')

# TODO:(byronk):
# a hack for now. Should look this up in labconfig_data. crbug.com/225108
# TODO:(byronk):
# replace SystemError with a specific exception crbug.com/225127


class BasicPrologixTest(unittest.TestCase):
    """
    Basic connection test
    """

    def test_bad_ip_address(self):
        """
        Connect to the wrong port and check for the right error message.
        """
        instr = copy.copy(scpi_instruments['pxt'])
        instr['ip'] = '192.168.0.0'  # str(int(instr['gpib_addr'])+1)
        log.debug(instr)
        instr_dict = {'inst': instr}
        with self.assertRaises(Exception) as ex:
            self._get_idns_and_verify(instruments=instr_dict, opc=True)
        self.assertIsInstance(ex.exception,
                              wireless_automation_error.SocketTimeout)

    # def test_ConnectToPortBadIP(self):
    #     """ Make a socket connection """
    #     with self.assertRaises(Exception) as ex:
    #         prologix_scpi_driver.connect_to_port('192.168.255.111', 1234, 1)
    #     self.assertIsInstance(ex.exception,
    #                           wireless_automation_error.SocketTimeout)

    def test_BadGpibAddress(self):
        """
        How does the code behave if we can't connect.
        """
        instr = copy.copy(scpi_instruments['pxt'])
        instr['gpib_addr'] = 9  # str(int(instr['gpib_addr'])+1)
        instr_dict = {'inst': instr}
        ext_type = wireless_automation_error.InstrumentTimeout
        with self.assertRaises(ext_type) as ex:
            self._get_idns_and_verify(instruments=instr_dict, opc=True)

    @mock.patch.object(prologix_scpi_driver.PrologixScpiDriver, '_direct_query')
    def test_NonClearReadBufferBeforeInit(self, patched_driver):
        """
        Sometimes the Prologix box will have junk in it's read buffer
        There is code to read the junk out until setting the ++addr works.
        Test that here.
        """
        instr = scpi_instruments['pxt']
        patched_driver.side_effect = ['junk1', 'junk2', instr['gpib_addr']]
        driver = prologix_scpi_driver.PrologixScpiDriver(
            hostname=instr['ip'],
            port=instr['port'],
            gpib_address=instr['gpib_addr'],
            read_timeout_seconds=2)

    def test_Reset(self):
        for instr in scpi_instruments.values():
            scpi_connection = self._open_prologix(instr, opc_on_stanza=True,
                                                  read_timeout_seconds=20)
            scpi_connection.query("*IDN?")
            self.scpi_connection.close()

    def test_FetchErrors(self):
        """
        call FetchErrors
        """
        for instr in scpi_instruments.values():
            scpi_connection = self._open_prologix(instr, opc_on_stanza=True,
                                                  read_timeout_seconds=2)
            scpi_connection.retrieve_errors()
            self.scpi_connection.close()

    def test_BadScpiCommand(self):
        """
        Send a bad command. We should fail gracefully.
        """
        for instr in scpi_instruments.values():
            log.debug('Trying bad command on device : %s ' % instr)
            scpi_connection = self._open_prologix(instr, opc_on_stanza=True,
                                                  read_timeout_seconds=2)
            try:
                scpi_connection.query('*IDN')
            except wireless_automation_error.InstrumentTimeout:
                assert ("Should have raised an Instrument Timeout "
                        "on a bad SCPI command")

    def test_GetIdnOpcTrue(self):
        """
        Test with opc True. OPC= operation complete. Asking this
        question *OPC? after commands blocks until the command finishes.
        This prevents us from sending commands faster then then the
        instrument can handle. True is usually the right setting.

        """
        self._get_idns_and_verify(instruments=scpi_instruments, opc=True)

    def test_GetIdnOpcFalse(self):
        """
        Now with OPC off.
        """
        self._get_idns_and_verify(instruments=scpi_instruments, opc=False)

    def _open_prologix(self, instr, opc_on_stanza, read_timeout_seconds=2):
        """
        Build the prologix object.
        """
        ip_addr = instr['ip']
        name_part = instr['name']
        gpib_addr = instr['gpib_addr']
        port = instr['port']
        log.debug("trying %s at %s" % (name_part, ip_addr))
        driver = prologix_scpi_driver.PrologixScpiDriver(
            hostname=ip_addr,
            port=port,
            gpib_address=gpib_addr,
            read_timeout_seconds=read_timeout_seconds)
        self.scpi_connection = driver
        return self.scpi_connection

    def _get_idns_and_verify(self, instruments, opc=False):
        """
        Get the idn string from all the instruments, and check that it
        contains the desired substring. This is a quick sanity check only.
        """
        for instr in instruments.values():
            scpi_connection = self._open_prologix(instr, opc_on_stanza=opc)
            response = scpi_connection.query('*IDN?')
            log.debug("looking for %s  in response string: %s " %
                      (instr['name'], response))
            assert instr['name'] in response
            self.scpi_connection.close()

if __name__ == '__main__':
    unittest.main()

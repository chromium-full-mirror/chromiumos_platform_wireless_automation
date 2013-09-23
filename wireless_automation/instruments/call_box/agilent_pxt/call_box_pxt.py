# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The PXT specific call box
"""

import time

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.instruments.call_box import call_box_interface
from wireless_automation.instruments.prologix import prologix_scpi_driver


class CallBoxPxt(call_box_interface.CallBoxInterface):
    """
    Object for the Agilent PXT, the LTE call box.
    """
    # CONFIGSPEC is inherited from the Interface.
    # List of possible call status. Used in the CallBoxFakePxt
    # to give correct answers, but stored here to keep all the
    # PXT knowledge in one place.
    ALL_STATES = ['STOP', 'OFF', 'IDLE', 'CON', 'REG', 'LOOP', 'REL', 'UNAV']
    IDLE_STATES = ['STOP', 'IDLE', 'OFF']
    CONNECTED_STATES = ['CON']
    EXAMPLE_ID_STRING = "Agilent Technologies,E6621A,MY51100107,6.4.0.7"
    MATCH_IN_EXAMPLE_ID_STRING = 'E6621'

    def __init__(self, config):
        super(CallBoxPxt, self).__init__(config)
        self.scpi = prologix_scpi_driver.PrologixScpiDriver(
            hostname=config['scpi_ip_address'],
            port=config['port'],
            gpib_address=config['gpib_address'],
            read_timeout_seconds=config['read_timeout_seconds'],
            connect_timeout_seconds=config['connect_timeout_seconds']
        )
        # Make sure we can talk to it, and it's the right box
        assert self.MATCH_IN_EXAMPLE_ID_STRING in self.get_id()

    def get_id(self):
        return self.scpi.query("*IDN?")

    def reset(self):
        self.scpi.send_list(['*RST?'])

    def turn_rf_on(self):
        raise NotImplementedError

    def turn_rf_off(self):
        raise NotImplementedError

    def is_rf_on(self):
        raise NotImplementedError

    def is_idle(self):
        state = self.scpi.query('BSE:SIMULator?')
        return state in self.IDLE_STATES

    def close(self):
        self.scpi.close()

    def is_connected(self):
        return self._get_cell_status() in self.CONNECTED_STATES

    def _get_cell_status(self):
        status = self.scpi.query('BSE:STATus:ACELL?')
        return status

    def set_power_dbm(self, dbm):
        self.scpi.send_list(['AMPLitude:ALL %s' % dbm])

    def get_power_dbm(self):
        return float(self.scpi.query('AMPLitude:ALL?'))

    def start(self):
        commands = [
            '*CLS',
            'STATus:PRESet',
            # Enable conn checks
            'BSE:CONFig:RRC:CTIMer:STATus ON',
            # Check freq (secs)
            'BSE:CONFig:RRC:CTIMer:LENGth 5',
            'SIGN:MODE BSE',
            'SCENArio:LOAD "FDD_Combined_v6.3.lbmf"',
            'BSE:CONF:PROF 20MH',
            'FREQ:BAND 13',
            'BSE:SIMULator RUN'
        ]
        self.scpi.send_list(commands)

    def stop(self):
        self.scpi.send_list(['BSE:SIMULator STOP'])
        # Make sure the call status goes to idle before continuing.
        for i in range(10):
            if self.is_idle():
                return
            time.sleep(1)
        raise wireless_automation_error.InstrumentTimeout(
            'PXT::Stop did not produce an idle state '
            'Idle State: %s' % self.IDLE_STATES)

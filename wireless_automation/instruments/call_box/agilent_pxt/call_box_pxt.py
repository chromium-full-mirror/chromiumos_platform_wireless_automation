# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The PXT specific call box
"""

import time

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.instruments.call_box import call_box_interface
from wireless_automation.instruments.call_box import call_box_fake
from wireless_automation.instruments.prologix import prologix_scpi_driver


class CallBoxPxt(call_box_interface.CallBoxPxtInterface):
    """
    Object for the Agilent PXT, the LTE call box.
    """
    # CONFIGSPEC is inherited from the Interface.
    # List of possible call status. Used in the CallBoxFakePxt
    # to give correct answers, but stored here to keep all the
    # PXT knowledge in one place.

    def __new__(cls, config):
        """
        Call Box Factory. Rreturn the dummy class if fake_hardware
        is true, otherwise return an object of this class.
        :param cls:
        :param config:
        :return:
        """
        assert isinstance(config['fake_hardware'], bool)
        if config['fake_hardware']:
            fake = call_box_fake.CallBoxFakePxt(config)
            return fake
        else:
            return super(CallBoxPxt, cls).__new__(cls, config)
            #return cls.__new__(cls, config)

    def __init__(self, config):
        super(CallBoxPxt, self).__init__(config)
        self.log.info('Constructing : %s' % self.__class__)
        self.scpi = prologix_scpi_driver.PrologixScpiDriver(
            hostname=self.scpi_ip_address,
            port=self.scpi_ip_port,
            gpib_address=self.gpib_address,
            read_timeout_seconds=self.read_timeout_seconds,
            connect_timeout_seconds=self.connect_timeout_seconds
        )
        # Make sure we can talk to it, and it's the right box
        assert self.MATCH_IN_EXAMPLE_ID_STRING in self.get_id()

    def get_id(self):
        return self.scpi.query("*IDN?")

    def reset(self):
        self.scpi.send_list(['*RST?'])

    def turn_rf_on(self):
        """
        Turns both RF port on.
        :return: None.
        """
        self.scpi.send('rfoutput1:state on')
        self.scpi.send('rfoutput2:state on')

    def turn_rf_off(self):
        """
        Turns both RF port off.
        :return: None.
        """
        ret1 = self.scpi.send('rfoutput1:state off')
        ret2 = self.scpi.send('rfoutput2:state off')

    def is_rf_on(self):
        ret1 = self.scpi.query('rfoutput1:state?')
        ret2 = self.scpi.query('rfoutput2:state?')
        return ret1.lower() == 'on' and ret2.lower == 'on'

    def is_idle(self):
        state = self.scpi.query('BSE:SIMULator?')
        return state in self.IDLE_STATES

    def close(self):
        self.scpi.close()
        time.sleep(.5)  # Enough to let the prologix adapter to disconnect

    def is_connected(self):
        return self._get_cell_status() in self.CONNECTED_STATES

    def is_registered(self):
        return self._get_cell_status() in self.REGISTERED_STATES

    def _get_cell_status(self):
        """
        :return: The cell state, a value from self.ALL_STATES
        """
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
            # These two have to be done before loading
            'SCENArio:LOAD "FDD_Combined_v6.3.lbmf"',
            'BSE:CONFig:NAS:DEFault:EBConfig1:ADDRess:V4 "%s"' %
                 self.dut_ip_address,
            'BSE:CONFig:NAS:DEFault:EBConfig1:APN "%s"' % self.apn_name,
            'BSE:CONFig:NAS:MCC %s' % self.mcc,
            'BSE:CONFig:NAS:MNCDigits %s' % self.mnc_digits,
            'BSE:CONFig:NAS:MNC %s' % self.mnc,
            'BSE:EPC EMBed',
            'BSE:CONF:PROFile %sMH' % self.bandwidth_mhz,
            'FREQ:BAND %s' % self.band,
            'BSE:CONFig:PHY:UL:GRANT:SPS:RB:START %s' %
                 self.resource_block_start,
            'BSE:CONFig:PHY:UL:GRANT:SPS:RB:SIZE %s' % self.resource_block_stop,
            'BSE:CONF:PHY:UL:GRANT:MODE %s' % self.tx_data_mode,
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

    def __del__(self):
        try:
            self.scpi.close()
        # If the tear down process has already removed the scpi object
        except AttributeError:
            pass

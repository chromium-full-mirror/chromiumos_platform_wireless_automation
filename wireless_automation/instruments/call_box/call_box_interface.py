# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
An interface for cellular call boxes.
"""

from wireless_automation.aspects import configurable


#pylint: disable=too-many-instance-attributes
# These classes have methods defined in their subclasses, but
# pylint doesn't see that.
#pylint: disable=abstract-method
class CallBoxBaseInterface(configurable.Configurable):
    """
    An interface for cellular call boxes.
    """
    CONFIGSPEC = [
        '#  Do not use real hardware, use a minimal fake',
        'fake_hardware=boolean(default=False)',
        '# Keep state or reset CallBox when constructed.',
        '# Useful for staring a test and keeping the call box in its state',
        '# on_init=option("maintain_state",'
                          ' "reset_state",default="reset_state")',
        '# Setup the SCPI adapter on the CallBox ',
        'scpi_ip_address=ip_addr(default=None)',
        'scpi_ip_port=integer(default=1234)',
        '# The GPIB address the SCPI adapter thinks the CallBox is on',
        'gpib_address=integer(min=0, max=999, default=14)',
        'read_timeout_seconds=integer(min=0, max=100, default=3)',
        'connect_timeout_seconds=integer(min=0, max=100, default=10)',
        '# Setup the CallBox',
        'band=integer(min=0, max=100, default=13)',
        'apn_name=string(default="internet")',
        'mnc=string(default="01")',  # Try 010 for Spring
        'mnc_digits=integer(min=2,max=3,default=2)',
        'mcc=string(default="001")',
        '#  The IP assigned to the DUT by the CallBox',
        'dut_ip_address=ip_addr(default="192.168.88.51")'
    ]
    ALL_STATES = []              # List of possible states
    IDLE_STATES = []             # The states that mean it's idle
    REGISTERED_STATES = []
    CONNECTED_STATES = []        # The states that count as connected
    EXAMPLE_ID_STRING = "CallBoxBaseInterface"  # The ID string *IDN? returns
    MATCH_IN_EXAMPLE_ID_STRING = 'Interface'

    def __init__(self, config):
        super(CallBoxBaseInterface, self).__init__(config)
        self.fake_hardware = config['fake_hardware']
        self.scpi_ip_address = config['scpi_ip_address']
        self.scpi_ip_port = config['scpi_ip_port']
        self.gpib_address = config['gpib_address']
        self.read_timeout_seconds = config['read_timeout_seconds']
        self.connect_timeout_seconds = config['connect_timeout_seconds']
        self.band = config['band']
        self.apn_name = config['apn_name']
        self.mnc = config['mnc']
        self.mnc_digits = config['mnc_digits']
        self.mcc = config['mcc']
        self.dut_ip_address = config['dut_ip_address']

    def get_id(self):
        """
        Returns the *IDN of the call box.

        """
        raise NotImplementedError

    def reset(self):
        """
        Returns the call box to a nearly powered on state. *RST and *CLS.
        """
        raise NotImplementedError

    def is_idle(self):
        """
        Returns true if the the call_state is in call_idle_states

        """
        raise NotImplementedError

    def close(self):
        """
        Closes the communications channel that is being used to talk to the
        instrument.

        """
        raise NotImplementedError

    def is_connected(self):
        """
        Returns true if the the call_state is in CONNECTED_STATES

        """
        raise NotImplementedError

    def is_registered(self):
        """
        Returns true if the the call_state is in REGISTERED_STATES

        """
        raise NotImplementedError

    def set_power_dbm(self, dbm):
        """
        Sets the RF power transmitting from the call box. In dBm.

        """

        raise NotImplementedError

    def get_power_dbm(self):
        """
        Gets the RF power transmitting from the call box.

        @return: power, in dBm.
        """

        raise NotImplementedError

    def is_rf_on(self):
        """
        Queries if the RF is turned on. The RF power can be high, but
        the RF port can be off.

        """

        raise NotImplementedError

    def turn_rf_on(self):
        """
        Turns on the RF ports of the call box.

        """

        raise NotImplementedError

    def turn_rf_off(self):
        """
        Turns off the RF ports of the call box.

        """

        raise NotImplementedError

    def start(self):
        """
        Loads all the needed configs to the call box, so a dut can connect.

        """

        raise NotImplementedError

    def stop(self):
        """
        Stops the call box, duts connected to it will see a call drop.
        """

        raise NotImplementedError

LTE_CONFIGSPEC = [
    '#  LTE specific settings',
    'resource_block_start=integer(min=0,max=100,default=0)',
    'resource_block_stop=integer(min=0,max=100,default=100)',
    'bandwidth_mhz=option("1.4","3","5","10","15","20",default="10")',
    'tx_data_mode=option("auto","fixed_mac_padding",default="auto")'
]


class CallBoxLteInterface(CallBoxBaseInterface):
    """
    Paramaters are added here for all call box's with LTE
    """
    CONFIGSPEC = CallBoxBaseInterface.CONFIGSPEC + LTE_CONFIGSPEC

    def __init__(self, config):
        super(CallBoxLteInterface, self).__init__(config)
        self.resource_block_start = config['resource_block_start']
        self.resource_block_stop = config['resource_block_stop']
        self.bandwidth_mhz = config['bandwidth_mhz']
        self.tx_data_mode = config['tx_data_mode']


#pylint: disable=interface-not-implemented
class CallBoxPxtInterface(CallBoxLteInterface):
    """
    This defines the internal states for both the Pxt and it's Fake.
    """
    base_configspec = CallBoxLteInterface.CONFIGSPEC
    CONFIGSPEC = configurable.list_to_configspec(base_configspec)
    CONFIGSPEC['scpi_ip_address'] = "ip_addr(default='172.22.50.244')"

    ALL_STATES = ['STOP', 'OFF', 'IDLE', 'CON', 'REG', 'LOOP', 'REL', 'UNAV']
    IDLE_STATES = ['STOP', 'IDLE', 'OFF']
    REGISTERED_STATES = ['REG']
    CONNECTED_STATES = ['CON']
    EXAMPLE_ID_STRING = "Agilent Technologies,E6621A,MY51100107,6.4.0.7"
    MATCH_IN_EXAMPLE_ID_STRING = 'E6621'


HSPA_CONFIGSPEC = ['# HSPA and HSPA + settings here',
                   '# More settings ']


class CallBoxHspa3gInterface(CallBoxBaseInterface):
    """
    Adding the 3G config parameters.
    """
    CONFIGSPEC = CallBoxLteInterface.CONFIGSPEC + HSPA_CONFIGSPEC

    def __init__(self, config):
        CallBoxBaseInterface.__init__(config)


class CallBoxLteHspa3gInterface(CallBoxBaseInterface):
    """
    Adding the HSPA and the 3G paramaters
    """
    CONFIGSPEC = CallBoxLteInterface.CONFIGSPEC + \
        LTE_CONFIGSPEC + HSPA_CONFIGSPEC

    def __init__(self, config):
        # LTE settings
        CallBoxBaseInterface.__init__(config)
        self.resource_block_start = config['resource_block_start']
        self.resource_block_stop = config['resource_block_stop']
        self.bandwidth_mhz = config['bandwidth_mhz']
        self.tx_data_mode = config['tx_data_mode']
        # HSPA Settings

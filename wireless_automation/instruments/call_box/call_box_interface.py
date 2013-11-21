# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
An interface for cellular call boxes.
"""

from wireless_automation.aspects import configurable


class CallBoxInterface(configurable.Configurable):
    """
    An interface for cellular call boxes.
    """
    CONFIGSPEC = [
        'channel=integer(min=0, max=9999, default=1)',
        'scpi_ip_address=ip_addr(default=None)',
        'port=integer(default=1234)',
        'gpib_address=integer(min=0, max=999, default=14)',
        'read_timeout_seconds=integer(min=0, max=100, default=3)',
        'connect_timeout_seconds=integer(min=0, max=100, default=10)'
    ]
    ALL_STATES = []              # List of possible states
    IDLE_STATES = []             # The state that means it's idle
    REGISTERED_STATES = []
    CONNECTED_STATES = []        # The states that count as connected
    EXAMPLE_ID_STRING = "CallBoxInterface"  # The ID string *IDN? returns
    MATCH_IN_EXAMPLE_ID_STRING = 'Interface'

    def __init__(self, config):
        super(CallBoxInterface, self).__init__(config)

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

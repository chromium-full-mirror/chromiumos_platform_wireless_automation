# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
A dummy modem class, to provide modem functionality on workstations that
have no modems.
"""

from wireless_automation.duts import modem_interface


class DummyModem(modem_interface.ModemInterface):
    """
    A dummy modem class.

    """
    CONFIGSPEC = ['name = string(default="DummyMode")']

    def __init__(self, config):
        """
        @param config: a Config object.
        """
        super(DummyModem, self).__init__(config)

    def power_on(self):
        """
        Turn on a powered modem.
        """
        pass

    def power_off(self):
        """
        Turn off the modem, but do not disconnect the power lines.
        """
        pass

    def register(self):
        """
        Register with the network.
        """
        pass

    def deregister(self):
        """
        Deregister with the network.
        """
        pass

    def connect(self):
        """
        Connect
        """

        pass

    def disconnect(self):
        """
        Disconnect from the network.
        """
        pass

    def go_to_low_power(self):
        """
        Put the modem to sleep.
        @return:
        """
        pass

    def hard_power_cycle(self, block=True):
        """
        Powers off the modem by killing the power lines to it.
        Or as close to that as possible. This should be a
        the hardest reset available. Then powers the modem back up.
        This blocks until the modem is responsive.

        @block: return only after the modem responsive
        """
        pass

    def is_modem_there(self):
        """
        Can the modem be reached. If the modem is off or
        non responsive, returns a False.
        @return: Boolean.
        """
        pass

    def config_for_pxt(self):
        """
        Configs the modem to talk to the PXT call box.
        """
        pass

# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Base class for all modems.
"""

from wireless_automation.aspects import configurable


class ModemInterface(configurable.Configurable):
    """
    A base class for controlling the modem.

    """

    def __init__(self, config):
        """
        @param config: Config object.
        """
        super(ModemInterface, self).__init__(config)

    def power_on(self):
        """
        Turn on a powered modem.
        """
        raise NotImplementedError

    def power_off(self):
        """
        Turn off the modem, but do not disconnect the power lines.
        """
        raise NotImplementedError

    def register(self):
        """
        Register with the network.
        """
        raise NotImplementedError

    def deregister(self):
        """
        Deregister with the network.
        """
        raise NotImplementedError

    def connect(self):
        """
        Connect
        """

        raise NotImplementedError

    def disconnect(self):
        """
        Disconnect from the network.
        """
        raise NotImplementedError

    def go_to_low_power(self):
        """
        Put the modem to sleep.
        @return:
        """
        raise NotImplementedError

    def hard_power_cycle(self, block=True):
        """
        Powers off the modem by killing the power lines to it.
        Or as close to that as possible. This should be a
        the hardest reset available. Then powers the modem back up.
        This blocks until the modem is responsive.

        @block: return only after the modem responsive
        """
        raise NotImplementedError

    def is_modem_there(self):
        """
        Can the modem be reached. If the modem is off or
        non responsive, returns a False.
        @return: Boolean.
        """
        raise NotImplementedError

    def config_for_pxt(self):
        """
        Configs the modem to talk to the PXT call box.
        """
        raise NotImplementedError

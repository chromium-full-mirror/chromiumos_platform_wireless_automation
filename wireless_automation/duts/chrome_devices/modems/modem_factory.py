# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
A factory that returns the right modem for the device we are running on
"""

from wireless_automation.aspects import configurable
from wireless_automation.duts import dummy_modem


class ModemFactory(configurable.Configurable):
    """
    A class to return the right modem.
    This holds the magic to detect what modem is in use
    on the machine this code is running on. No config
    is needed, just ask this factory for a modem,
    and you get the right one, including a fake if there
    is no hardware modem.
    """
    def __init__(self, config):
        super(ModemFactory, self).__init__(config)

    @classmethod
    def get_modem(cls):
        """
        @return: the driver for the modem on this system.
        """
        config = dummy_modem.DummyModem.get_default_config()
        return dummy_modem.DummyModem(config)

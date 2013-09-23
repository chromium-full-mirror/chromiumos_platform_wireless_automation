# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
How to build the right dut
"""

from wireless_automation.aspects.wireless_automation_logging import \
    setup_logging
from wireless_automation.chrome_device import chrome_device_base
from wireless_automation.chrome_device.modems import modem_factory


class ChromeDeviceFactory(object):
    """
    TODO:
    A place holder, this class should return an object composed
    of all the objected needed to talk to the chromebook systems:
    shill, modemmanager, the modem direct, open and close switch,
    power reporting, etc.
    """
    log = setup_logging('ChromeDevice')

    def __init__(self):
        pass

    @classmethod
    def get_chrome_device(cls):
        """
        @param cls: The class.
        @return: A ChromeDevice with it's inner parts populated
        """
        cls.log.info('making new Chrome Device')
        # Only one choice now.
        config = chrome_device_base.ChromeDevice.get_default_config()
        modem = modem_factory.ModemFactory.get_modem()
        device = chrome_device_base.ChromeDevice(config)
        device.modem = modem
        return device

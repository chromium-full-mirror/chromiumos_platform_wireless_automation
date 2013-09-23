# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
How to build the right dut
"""

from wireless_automation.aspects import configurable
from wireless_automation.aspects.wireless_automation_logging import \
    setup_logging
from wireless_automation.duts import dut_interface
from wireless_automation.duts.chrome_devices.modems import modem_factory


class DutFactory(configurable.Configurable):
    """
    Composes a DUT from the parts specified in the config.
    """
    CONFIGSPEC = \
        ['type=option("chrome","android","iOS",default="chrome")'] + \
        configurable.nest_configspecs([
            ('DutInterface', dut_interface.DutInterface)
        ])
    log = setup_logging('DutInterface')

    def __init__(self, config):
        super(DutFactory, self).__init__(config)

    @classmethod
    def get_dut(cls):
        """
        @param cls: The class.
        @return: A DutInterface with it's inner parts populated
        """
        cls.log.info('making new Chrome Device')
        # Only one choice now.
        config = dut_interface.DutInterface.get_default_config()
        modem = modem_factory.ModemFactory.get_modem()
        device = dut_interface.DutInterface(config)
        device.modem = modem
        return device


def build_one(config):
    """
    Dut factory function.
    @param config:
    @return:
    """
    factory = DutFactory(config)
    return factory.get_dut()

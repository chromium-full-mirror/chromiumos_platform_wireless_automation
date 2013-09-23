# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import logging
import os
import subprocess
import time
import unittest

from wireless_automation.aspects.wireless_automation_logging import \
from wireless_automation.chrome_device.modems.altair import AltairLteModem
    setup_logging

log = setup_logging('AltairModemTest')

class FakeSerial(object):
    def __init__(self):
        pass


class test_altair_modem(unittest.TestCase):
    """

    """
    log = setup_logging('AltairModemTestWithHardware')

    def setUp(self):
        log = setup_logging('AltairModem', level=logging.DEBUG)
        config = AltairLteModem.get_default_config()
        self.modem = AltairLteModem(config)

    def tearDown(self):
        self.modem.close()

    def setup_from_fresh_boot(self):
        os.system('stop modemmanager')
        os.system('mount -o remount,rw /')

    def test_is_modem_there_returns_true(self):
        assert self.modem.is_modem_there()

    def test_bad_command_returns_false(self):
        assert not self.modem._send_at_command('xxxx')

    def xtest_modem_power_cycle_produces_talking_modem(self):
        assert self.modem.is_modem_there()
        self.modem.power_cycle()
        assert self.modem.is_modem_there()

    def test_config_for_pxt_works(self):
        self.modem.config_for_pxt()
        assert self.modem.is_modem_there()

if __name__ == '__main__':
    unittest.main()

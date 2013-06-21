# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from wireless_automation.chrome_device.modems.altair import AltairLteModem
from wireless_automation.aspects.wireless_automation_logging import \
    setup_logging
import unittest

log = setup_logging('AltairModemTest')

class test_altir_modem(unittest.TestCase):
    """

    """
    def test_restart(self):
        """

        """
        modem = AltairLteModem()
        modem.power_cycle()

if __name__ == '__main__':
    unittest.main()

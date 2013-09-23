# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from wireless_automation.duts.chrome_devices.modems import modem_factory


class TestsModemFactory(unittest.TestCase):
    """
    Test the modem factory.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_make_one(self):
        one = modem_factory.ModemFactory.get_modem()
        print one

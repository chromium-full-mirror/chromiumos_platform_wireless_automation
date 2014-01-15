# Copyright (c) 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
Testing the chrome dut object, with real hardware
"""

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.duts import chrome_dut

import unittest


class test_chrome_dut(unittest.TestCase):
    """
    Test the chrome dut with real hardware
    """
    def setUp(self):
        # Build a DUT
        dut_config = chrome_dut.ChromeDut.get_default_config()
        self.dut = chrome_dut.ChromeDut(dut_config, low_level_modem_driver=None)

    def test_localhost_iperf_with_no_server_raises_connection_failure(self):
        with self.assertRaises(wireless_automation_error.ConnectionFailure):
            results = self.dut.run_iperf_throughput_test('10.0.0.1')

    def test_localhost_iperf_with_server_returns_high_throughput(self):
        self.dut.start_local_iperf_server()
        results = self.dut.run_iperf_throughput_test('localhost',
                                                     transfer_seconds=3)
        assert results > 100

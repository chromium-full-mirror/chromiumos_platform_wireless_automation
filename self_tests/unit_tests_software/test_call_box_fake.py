# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.instruments.call_box.call_box_fake import \
    CallBoxFakePxt

log = wireless_automation_logging.setup_logging('call_box_pxt')


class test_fake_pxt(unittest.TestCase):
    """
    Test the PXT class
    """
    def setUp(self):
        self.config = CallBoxFakePxt.get_default_config()
        self.pxt = CallBoxFakePxt(self.config)

    def test_start_and_stop_should_change_state(self):
        """
        test_start_and_stop_should_change_state
        """
        assert self.pxt._get_cell_status() in self.pxt.IDLE_STATES
        assert self.pxt.is_idle()
        self.pxt.start()
        assert not self.pxt.is_idle()
        assert self.pxt._get_cell_status() in self.pxt.CONNECTED_STATES
        assert self.pxt.is_connected()
        self.pxt.stop()
        assert not self.pxt.is_connected()
        assert self.pxt._get_cell_status() in self.pxt.IDLE_STATES
        self.pxt.close()

    def test_reset_clears_rf_on(self):
        """
        test reset
        """
        self.pxt.turn_rf_on()
        assert self.pxt.is_rf_on() is True
        self.pxt.reset()
        assert self.pxt.is_rf_on() is False

    def test_get_id(self):
        """
        test get_id
        """
        self.pxt.get_id()

    def test_set_and_read_power(self):
        """
        test_set_and_read_power
        """
        power = -82
        self.pxt.set_power_dbm(power)
        assert self.pxt.get_power_dbm() == power

    def test_power_outside_range_should_raise(self):
        """
        test_power_outside_range_should_raise
        """
        power = -9999
        with self.assertRaises(wireless_automation_error.BadScpiCommand):
            self.pxt.set_power_dbm(power)
        power = 9999
        with self.assertRaises(wireless_automation_error.BadScpiCommand):
            self.pxt.set_power_dbm(power)

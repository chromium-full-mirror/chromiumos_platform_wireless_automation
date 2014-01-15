# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import mock
import unittest

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects.wireless_automation_logging import \
    setup_logging
from wireless_automation.instruments.call_box.agilent_pxt.call_box_pxt import \
    CallBoxPxt
from wireless_automation.instruments.call_box.call_box_fake import \
    CallBoxFakePxt

log = setup_logging('pxt_hardware_test')


class TestPxt(unittest.TestCase):
    """
    Test the PXT class.
    """

    def setUp(self):
        self.config = CallBoxPxt.get_default_config()
        self.config['scpi_ip_address'] = '172.22.50.236'

    def tearDown(self):
        self.pxt.close()

    def test_fake_hardware_returns_fake(self):
        """
        New of the pxt call box acts as a factory, and can return
        a fake if the config asks for it.
        This tests the new() function of the CallBoxPxt.
        """
        self.config['fake_hardware'] = True
        self.pxt = CallBoxPxt(self.config)
        assert isinstance(self.pxt, CallBoxFakePxt)

    def test_no_fake_hardware_returns_real_pxt(self):
        self.config['fake_hardware'] = False
        self.pxt = CallBoxPxt(self.config)
        assert isinstance(self.pxt, CallBoxPxt)

    def test_most_real_pxt_functions(self):
        """
        Test most function calls here. The startup
        cost to reset the PXT is high. So just
        do it once and have one large test function.

        """
        self.pxt = CallBoxPxt(self.config)
        self.pxt.reset()
        self.pxt.start()
        power = -57
        self.pxt.set_power_dbm(power)
        power_read = self.pxt.get_power_dbm()
        was_connected = self.pxt.is_connected()
        assert not self.pxt.is_idle()
        self.pxt.stop()
        assert self.pxt.is_idle()
        assert self.pxt.MATCH_IN_EXAMPLE_ID_STRING in self.pxt.get_id()
        self.pxt.close()
        assert power == power_read

    def test_stop_raises_when_it_does_not_go_idle(self):
        """
        test_stop_raises_when_it_does_not_go_idle
        """
        self.pxt = CallBoxPxt(self.config)
        #with mock.patch.object(self.pxt, 'is_idle'):
        self.pxt.is_idle = mock.MagicMock()
        self.pxt.is_idle.return_value = False
        self.pxt.scpi = mock.MagicMock()
        log.debug('PXT idle: %s ' % self.pxt.is_idle())
        with self.assertRaises(wireless_automation_error.InstrumentTimeout):
            self.pxt.stop()

# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from wireless_automation.racks import oyster_bay_rack


class TestOysterBayDevelopmentRack(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def test_make_a_real_one():
        config = \
            oyster_bay_rack.OysterBayPxtDevelopmentRack.get_default_config()
        one = oyster_bay_rack.OysterBayPxtDevelopmentRack(config)

    @staticmethod
    def test_make_a_fake_one():
        config = \
            oyster_bay_rack.OysterBayPxtDevelopmentRack.get_default_config()
        #config['CallBoxFactory']['call_box_type'] = 'fake'
        print '\n'.join(config.write())
        config['CallBoxFactory']['call_box_model'] = 'fake'
        one = oyster_bay_rack.OysterBayPxtDevelopmentRack(config)

    @staticmethod
    def test_composed_interface():
        config = \
            oyster_bay_rack.OysterBayPxtDevelopmentRack.get_default_config()
        print config


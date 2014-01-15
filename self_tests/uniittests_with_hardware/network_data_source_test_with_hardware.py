# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from wireless_automation.instruments.network_data_source \
    import network_data_source


class TestNetworkDataSource(unittest.TestCase):

    def setUp(self):
        config = network_data_source.NetworkDataSource.get_default_config()
        self.ds = network_data_source.NetworkDataSource(config)

    def tearDown(self):
        pass

    def test_make_one(self):
        # setUp does this
        pass

    def test_start_stop_should_not_raise(self):
        self.ds.start()
        self.ds.stop()

    def test_get_ip_address(self):
        self.ds.ip_address

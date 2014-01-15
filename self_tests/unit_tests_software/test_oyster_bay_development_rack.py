# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest
import subprocess

from wireless_automation.racks import rack_with_lte_and_data_source


class LocalIperf(object):

    def __init__(self, config):
        self.iperf_process = None
        self.config = config

    def __enter__(self):
        self.iperf_process = subprocess.Popen(['iperf', '-s'])
        self.config['NetworkDataSource']['ip_address'] = '127.0.0.1'
        return self

    def __exit__(self, the_type, value, tracebaack):
        self.iperf_process.terminate()
        return True


class TestOysterBayDevelopmentRack(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def test_make_a_real_one():
        config = rack_with_lte_and_data_source.\
            OysterBayPxtDevelopmentRack.get_default_config()
        # Make this run against the local machine
        with LocalIperf(config) as liperf:
            one = rack_with_lte_and_data_source.\
                OysterBayPxtDevelopmentRack(liperf.config)

    @staticmethod
    def test_make_a_fake_one():
        config = rack_with_lte_and_data_source.\
            OysterBayPxtDevelopmentRack.get_default_config()
        config['NetworkDataSource']['fake_hardware'] = True
        config['LteCallBox']['fake_hardware'] = True
        one = rack_with_lte_and_data_source.\
            OysterBayPxtDevelopmentRack(config)
        assert True

    @staticmethod
    def test_composed_interface():
        config = rack_with_lte_and_data_source.\
            OysterBayPxtDevelopmentRack.get_default_config()

    @staticmethod
    def test_start_a_real_pxt():
        config = rack_with_lte_and_data_source.\
            OysterBayPxtDevelopmentRack.get_default_config()
        with LocalIperf(config) as cfg:
            one = rack_with_lte_and_data_source.\
                OysterBayPxtDevelopmentRack(cfg.config)
            one.call_box.start()

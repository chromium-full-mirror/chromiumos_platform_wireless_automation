# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest
import subprocess

from wireless_automation.racks import oyster_bay_rack


class LocalIperf(object):

    def __init__(self, config):
        self.iperf_process = None
        self.config = config

    def __enter__(self):
        self.iperf_process = subprocess.Popen(['/usr/bin/iperf', '-s'])
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
        config = \
            oyster_bay_rack.OysterBayPxtDevelopmentRack.get_default_config()
        # Make this run against the local machine
        with LocalIperf(config) as liperf:
            one = oyster_bay_rack.OysterBayPxtDevelopmentRack(liperf.config)

    @staticmethod
    def test_make_a_fake_one():
        config = \
            oyster_bay_rack.OysterBayPxtDevelopmentRack.get_default_config()
        config['CallBoxFactory']['call_box_type'] = 'fake'
        print '\n'.join(config.write())
        print config
        config['CallBoxFactory']['call_box_model'] = 'fake'
        config['NetworkDataSource']['fake'] = True
        one = oyster_bay_rack.OysterBayPxtDevelopmentRack(config)

    @staticmethod
    def test_composed_interface():
        config = \
            oyster_bay_rack.OysterBayPxtDevelopmentRack.get_default_config()
        print config

    @staticmethod
    def test_start_a_real_pxt():
        config = \
            oyster_bay_rack.OysterBayPxtDevelopmentRack.get_default_config()
        print '\n'.join(config.write())
        config['CallBoxFactory']['call_box_model'] = 'pxt'
        with LocalIperf(config) as cfg:
            one = oyster_bay_rack.OysterBayPxtDevelopmentRack(cfg.config)
            one.call_box.start()

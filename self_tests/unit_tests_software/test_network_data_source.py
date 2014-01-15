# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Test the network data source against real machines with iperf, and
testing error handling by trying machines that are not on the network.
"""

from wireless_automation.instruments.network_data_source import \
    network_data_source
from wireless_automation.aspects import wireless_automation_error
import unittest
import subprocess
import time


class LocalIperf(object):

    def __init__(self, config):
        self._iperf_process = None
        self.config = config

    def __enter__(self):
        self._iperf_process = subprocess.Popen(['iperf', '-s'])
        self.config['ssh_ip_address'] = '127.0.0.1'
        self.config['start_iperf_server'] = True
        self.config['start_netperf_server'] = True
        self.config['fake_hardware'] = True
        # Iperf take a bit to get going.
        time.sleep(0.5)
        return self

    def __exit__(self, exception_type, exception_value, tracebaack):
        self._iperf_process.terminate()


class TestNetworkDataSource(unittest.TestCase):

    def test_ping_unreachable_host_fails(self):
        """
        Test the ping function on an unreachable host
        """
        config = network_data_source.NetworkDataSource.get_default_config()
        with LocalIperf(config) as iperf:
            iperf.config['ssh_ip_address'] = '129.0.0.1'
            iperf.config['fake_hardware'] = False
            with self.assertRaises(wireless_automation_error.ConnectionFailure):
                nds = network_data_source.NetworkDataSource(iperf.config)

    def test_ping_local_host_passes(self):
        """
        Test the ping function with a localhost.
        """
        config = network_data_source.NetworkDataSource.get_default_config()
        with LocalIperf(config) as iperf:
            network_data_source.NetworkDataSource(iperf.config)

    def test_fake(self):
        """
        Fake out all hardware and run. This will run in a VM.
        """
        config = network_data_source.NetworkDataSource.get_default_config()
        with LocalIperf(config) as iperf:
            nds = network_data_source.NetworkDataSource(iperf.config)
            results = nds.run_iperf_download_test()
            assert results is not None
            print 'results:'
            print (results)

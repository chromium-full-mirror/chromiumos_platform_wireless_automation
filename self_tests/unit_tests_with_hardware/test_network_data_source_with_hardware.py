# Copyright (c) 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from wireless_automation.aspects import wireless_automation_error
from wireless_automation.duts import chrome_dut
from wireless_automation.instruments.network_data_source \
        import network_data_source


class TestNetworkDataSource(unittest.TestCase):

    def test_fake_hardware_should_not_raise_exception_on_bad_ip(self):
        config = network_data_source.NetworkDataSource.get_default_config()
        config['fake_hardware'] = True
        config['ssh_ip_address'] = '10.0.0.200'  # A bad IP
        config['start_iperf_server'] = True
        config['start_netperf_server'] = True
        self.ds = network_data_source.NetworkDataSource(config)
        self.ds.stop()

    def test_netperf_on_remote_chrome_dut(self):
        nds_config = network_data_source.NetworkDataSource.get_default_config()
        nds_config['start_iperf_server'] = False
        nds_config['start_netperf_server'] = True
        self.ds = network_data_source.NetworkDataSource(nds_config)

        #  Make a dut to test the network data source
        dut_config = chrome_dut.ChromeDut.get_default_config()
        dut = chrome_dut.ChromeDut(dut_config)
        server = nds_config['ssh_ip_address']
        mbps1 = dut.run_netperf_throughput_test(server, direction='uplink',
                                                transfer_seconds=3)
        self.assertGreater(mbps1, 0)
        mbps2 = dut.run_netperf_throughput_test(server, direction='downlink',
                                                transfer_seconds=3)
        self.assertGreater(mbps2, 0)
        self.ds.stop()

    def test_iperf_on_remote_chrome_dut(self):
        nds_config = network_data_source.NetworkDataSource.get_default_config()
        nds_config['start_iperf_server'] = True
        nds_config['start_netperf_server'] = False
        self.ds = network_data_source.NetworkDataSource(nds_config)

        #  Make a dut to test the network data source
        dut_config = chrome_dut.ChromeDut.get_default_config()
        dut = chrome_dut.ChromeDut(dut_config)
        server = nds_config['ssh_ip_address']
        mbps1 = dut.run_iperf_throughput_test(server, transfer_seconds=3,
                                              direction='uplink')
        self.assertGreater(mbps1, 0)
        mbps2 = dut.run_iperf_throughput_test(server, transfer_seconds=3,
                                              direction='downlink')
        self.assertGreater(mbps1, 0)
        self.ds.stop()

    def test_iperf_uplink_on_localhost_server(self):
        dut = self._get_default_dut()
        dut.start_local_iperf_server()
        mbps1 = dut.run_iperf_throughput_test('localhost', transfer_seconds=3,
                                              direction='uplink')
        self.assertGreater(mbps1, 0)

    def test_iperf_downlink_on_local_server(self):
        dut = self._get_default_dut()
        dut.start_local_iperf_server()
        mbps1 = dut.run_iperf_throughput_test('localhost', transfer_seconds=3,
                                              direction='downlink')
        self.assertGreater(mbps1, 0)

    def test_netperf_uplink_on_localhost_server(self):
        dut = self._get_default_dut()
        dut.start_local_netperf_server()
        mbps1 = dut.run_netperf_throughput_test('localhost', transfer_seconds=3,
                                                direction='uplink')
        self.assertGreater(mbps1, 0)

    def test_netperf_downlink_on_localhost_server(self):
        dut = self._get_default_dut()
        dut.start_local_netperf_server()
        mbps1 = dut.run_netperf_throughput_test('localhost', transfer_seconds=3,
                                                direction='downlink')
        self.assertGreater(mbps1, 0)

    def test_many_local_iperf_tests_in_a_row(self):
        dut = self._get_default_dut()
        dut.start_local_iperf_server(timeout_secs=100)
        for i in range(10):
            mbps1 = dut.run_iperf_throughput_test('localhost',
                                                  transfer_seconds=1,
                                                  direction='uplink')
            self.assertGreater(mbps1, 0)
            mbps1 = dut.run_iperf_throughput_test('localhost',
                                                  transfer_seconds=1,
                                                  direction='downlink')
            self.assertGreater(mbps1, 0)

    def test_many_local_netperf_tests_in_a_row(self):
        dut = self._get_default_dut()
        dut.start_local_netperf_server(timeout_secs=100)
        for i in range(10):
            mbps1 = dut.run_netperf_throughput_test('localhost',
                                                    transfer_seconds=1,
                                                    direction='uplink')
            self.assertGreater(mbps1, 0)
            mbps1 = dut.run_netperf_throughput_test('localhost',
                                                    transfer_seconds=1,
                                                    direction='downlink')
            self.assertGreater(mbps1, 0)

    def test_misspelled_direction_should_raise(self):
        dut = self._get_default_dut()
        with self.assertRaises(wireless_automation_error.BadExternalConfig):
            dut.run_netperf_throughput_test('localhost',
                                            transfer_seconds=1,
                                            direction='raise_on_this')

    def _get_default_dut(self):
        dut_config = chrome_dut.ChromeDut.get_default_config()
        return chrome_dut.ChromeDut(dut_config)

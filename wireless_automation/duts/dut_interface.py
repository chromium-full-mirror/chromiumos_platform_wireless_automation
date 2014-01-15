# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Base class for all modem_drivers
"""

from wireless_automation.aspects import configurable


class DutInterface(configurable.Configurable):
    """
    Interface definition for Devices Under Test. Could be Chromebooks,
    could be iOS phones, could be Android devices.
    """
    CONFIGSPEC = ['fake_hardware=boolean(default=False)']

    def __init__(self, config, low_level_modem_driver=None):
        """
        :param config:  ConfigObj that contains setup info
        :param low_level_modem_driver: driver to control the
            modem directly. Using this is optional, the dut
            has methods to control the modem. The driver is
            needed only when these methods are not detailed
            enough. The method stop
        :return:
        """
        super(DutInterface, self).__init__(config)
        self.modem = low_level_modem_driver
        self.fake_hardware = config['fake_hardware']

    def cellular_connect(self, technology):
        """
        Instruct the dut to connect it's cellular system
        to the specified technology.
        This is not a command given directly to the modem.
        This instruct the dut to use it's normal methods
        to establish a connection. In ChromeOS, this would
        be done by shill.
        :param technology:
        :return:
        """
        raise NotImplementedError

    def cellular_controllers_stop(self):
        """
        Turn off any software that may try to control the modem.
        Use this before using any modem driver.
        For example: in ChromeOS this stops Shill and ModemManager.
        """
        raise NotImplementedError

    def run_iperf_throughput_test(self, iperf_server_ip, iperf_port=5001,
                                  direction='uplink', seconds=10):
        """
        Run one iperf test from the device we are on to
        the iperf server running on iperf_server_ip.
        This assumes the server is ready and waiting.

        :param iperf_server_ip: Address of server
        :param seconds: seconds to run the test.
        :return: a dict of results.
        """
        raise NotImplementedError

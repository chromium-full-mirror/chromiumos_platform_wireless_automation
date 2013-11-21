# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Base class for all chrome_devices
"""

from wireless_automation.aspects import configurable


class DutInterface(configurable.Configurable):
    """
    Interface definition for Devices Under Test. Could be Chromebooks,
    could be iOS phones, could be Android devices.
    """
    CONFIGSPEC = ['modem_interface=option("altair","dummy",default="dummy")']

    def __init__(self, config):
        """
        @param config:  Configurable object.
        @return: DutInterface
        """
        super(DutInterface, self).__init__(config)
        self.modem = None

    @staticmethod
    def measure_download_speed(url):
        """
        @param url:  Where to download from.
        @return: Speed of the download
        """
        str(url)
        return 1

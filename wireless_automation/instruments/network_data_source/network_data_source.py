# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The data source for downloading data for speed tests and connectivity tests.
"""

from wireless_automation.aspects import configurable


class NetworkDataSource(configurable.Configurable):
    """
    A class to control a networked data source. Networking
    tests can be performed against this server to measure
    download speed.  We may support a simple http server,
    and an iperf server.

    Right now, this concept is implemented as a custom
    setup stumpy. Nobody has written down how it was setup.
    At some point, that setup should be stored here.
    """
    CONFIGSPEC = ["ip_address = ip_addr(default ='172.22.50.124')"]

    def __init__(self, config):
        """
        @param config:  Config object
        """
        super(NetworkDataSource, self).__init__(config)
        self.ip_address = config['ip_address']

    @staticmethod
    def start():
        """
        Starts the network server.
        """
        # todo: log this
        pass

    @staticmethod
    def stop():
        """
        Stops the network server.
        """
        pass

    @staticmethod
    def get_download_url():
        """
        Returns the URL to download from
        """
        pass

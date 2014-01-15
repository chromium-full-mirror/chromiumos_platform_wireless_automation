# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The data source for downloading data for speed tests and connectivity tests.
"""

import os
import pexpect
from wireless_automation.aspects import configurable
from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging


class LogIt(object):
    """
    A class to pass to pexpect that looks like stdout.
    This redirects pexpect's output to log.debug.
    """
    def __init__(self, logger):
        self.log = logger

    def write(self, message):
        """
        This looks like the write function of stdout, but
        redirect to the debug logger.
        """
        if not message:
            return
        self.log.debug(message.replace('\n', ' '))
        self.log.debug(message.replace('\r', ''))

    def flush(self):
        """
        Needed as part of the expected interface. For our
        logging needs, flushing isn't important.
        """
        pass


class NetworkDataSource(configurable.Configurable):
    #pylint: disable=too-many-instance-attributes
    """
    A class to control a networked data source. Networking
    tests can be performed against this server to measure
    download speed.  An iperf server is implemented.

    """
    CONFIGSPEC = ["# SSH connection params",
                  "ssh_ip_address = ip_addr()",
                  "ssh_port = integer(default=22)",
                  "password = string(default='test0000')",
                  "# Iperf server port",
                  '# The iperf/netperf ip address may be different then the',
                  '# ssh address, if the network data source has two',
                  '# ethernet interfaces',
                  "data_ip_address = ip_addr(default ='172.22.50.9')",
                  "iperf_port = integer(default=5001)",
                  "# Disable the iperf server bring up ",
                  "# if a server is pre configured",
                  'start_iperf_server = boolean(default=True)',
                  '# Netperf',
                  'start_netperf_server = boolean(default=True)',
                  "netperf_port = integer(default=5001)",
                  '# Time to run either a netperf or iperf test',
                  '# Fake all hardware. Will run in a VM',
                  'fake_hardware = boolean(default=false)',
                  ]

    def __init__(self, config):
        """
        :param config:  Config object
        """
        super(NetworkDataSource, self).__init__(config)
        self.log = wireless_automation_logging.setup_logging('NetDataSource')
        self.connection = None
        self.ssh_ip_address = config['ssh_ip_address']
        self.ssh_port = config['ssh_port']
        self.data_ip_address = config['data_ip_address']
        self.iperf_port = config['iperf_port']
        self.netperf_port = config['netperf_port']
        self.password = config['password']
        self.fake_hardware = config['fake_hardware']
        self.start_iperf_server = config['start_iperf_server']
        self.start_netperf_server = config['start_netperf_server']
        self._ping_host_or_raise(self.ssh_ip_address)
        self.connection = self._start_iperf_server_on_test_image()
        self.connection = self._start_netperf_server_on_remote_test_image()

    # pylint: disable=invalid-name
    def _start_netperf_server_on_remote_test_image(self):
        """
        Starts the iperf server. This method expects the machine
        to be running a chromeos test image. It makes assumptions
        about iperf and iptables, and the login that are true for
        chromeos test images.
        """
        if not self.start_netperf_server or self.fake_hardware:
            self.log.info('Not starting netperf...')
            return None
        # SSH will open an X11 window to prompt for the password.
        self.log.info('Starting iperf on network data server')
        os.environ['SSH_ASKPASS'] = '0'
        cmd = 'ssh -p %s -o StrictHostKeyChecking=no -o ' \
              'UserKnownHostsFile=/dev/null root@%s' % \
              (self.ssh_port, self.ssh_ip_address)
        self.log.debug(cmd)
        connection = pexpect.spawn(cmd, logfile=LogIt(self.log), timeout=5)
        connection.expect('(?i)password:')
        connection.sendline(self.password)
        connection.expect('#')
        self.log.info('Logging in to remote data source  '
                      ' to start netperf at %s' %
                      self.ssh_ip_address)
        connection.sendline('netserver -p %s' % self.netperf_port)
        try:
            connection.expect('(?i)starting', timeout=1)
        except pexpect.TIMEOUT:
            self.log.error("Sending the netserver command timed out. "
                           "Is netserver installed? ")
            raise
        #self.log.info(connection.before + connection.after)
        return connection

    def _start_iperf_server_on_test_image(self):
        """
        Starts the iperf server. This method expects the machine
        to be running a chromeos test image. It makes assumptions
        about iperf and iptables, and the login that are true for
        chromeos test images.
        """
        if not self.start_iperf_server or self.fake_hardware:
            self.log.info('Not starting iperf...')
            return None
        # SSH will open an X11 window to prompt for the password.
        self.log.info('Starting iperf on network data server')
        os.environ['SSH_ASKPASS'] = '0'
        cmd = 'ssh -p %s -o StrictHostKeyChecking=no -o '\
              'UserKnownHostsFile=/dev/null root@%s' % \
              (self.ssh_port, self.ssh_ip_address)
        self.log.debug(cmd)
        connection = pexpect.spawn(cmd, logfile=LogIt(self.log), timeout=5)
        connection.expect('(?i)password:')
        connection.sendline(self.password)
        connection.expect('#')
        self.log.info('Logging in to remote data source to start iperf at %s' %
                      self.ssh_ip_address)
        self.log.info('running on dut: killall -9 iperf ')
        connection.sendline('killall -9 iperf')
        connection.sendline('iptables -I INPUT -p tcp --dport 5001 -j ACCEPT')
        connection.sendline('iptables -I OUTPUT -p tcp --sport 5001 -j ACCEPT')
        connection.sendline('iperf -s --port %s &' % self.iperf_port)
        try:
            connection.expect('(?i)default', timeout=1)
        except pexpect.TIMEOUT:
            self.log.error("Sending the iperf command timed out. "
                           "Not installed? ")
            raise
        return connection

    def _ping_host_or_raise(self, ip_address):
        """
        Check to see if the iperf host is reachable.
        :return: Raises an exception if ping fails
        """
        if self.fake_hardware:
            self.log.debug("In Fake mode, don't actually ping")
            return
        cmd = "ping -c 1 -w 2 " + ip_address + " > /dev/null 2>&1"
        self.log.debug(cmd)
        response = os.system(cmd)
        if response == 0:
            self.log.debug('ping worked')
            return
        else:
            self.log.debug('ping failed')
            raise wireless_automation_error.ConnectionFailure(
                'iperf host is not responding to ping: %s ' % ip_address)

    def stop(self):
        """
        Calls the stop functions for iperf and netperf
        :return:
        """
        self.stop_iperf()
        self.stop_netperf()

    def stop_netperf(self):
        """
        Stop the netperf process on the remote data server
        :return:
        """
        self.log.info('Stopping and disconnecting from the network data server')
        if self.fake_hardware:
            self.log.info('Fake stopping netperf.')
            return
        # If we fail to finish the _start method, connection will be None.
        if not self.connection:
            return
        self.connection.sendline('killall netserver > /dev/null')

    def stop_iperf(self):
        """
        Stops the network server.
        """
        self.log.info('Stopping and disconnecting from the network data server')
        if self.fake_hardware:
            self.log.info('Fake stopping iperf.')
            return
        # If we fail to finish the _start method, connection will be None.
        if self.connection is None:
            return
        self.connection.sendline('kill $!')
        self.connection.sendline('killall iperf')
        self.connection.sendline('exit')

    def __del__(self):
        """
        Turn off iperf and disconnect from the remote when we get killed.
        :return: None
        """
        if self.fake_hardware:
            self.log.debug('Fake del.')
            return
        self.stop()

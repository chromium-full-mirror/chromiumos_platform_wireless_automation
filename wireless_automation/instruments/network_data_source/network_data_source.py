# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The data source for downloading data for speed tests and connectivity tests.
"""

from wireless_automation.aspects import configurable
from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging
import os
import pexpect
import subprocess

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
        self.log.debug(message)

    def flush(self):
        """
        Needed as part of the expected interface. For our
        logging needs, flushing isn't important.
        """
        pass


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
    CONFIGSPEC = ["ip_address = ip_addr(default ='172.22.75.35')",
                  "seconds = integer(default=10)",
                  "port = integer(default=5001)",
                  "password = string(default='test0000')",
                  '# Fake all hardware. Will run in a VM',
                  'fake_hardware = boolean(default=false)',
                  '# Disable the iperf server bring up if a server is pre configured',
                  'start_iperf_server = boolean(default=false)'
                  ]

    def __init__(self, config):
        """
        :param config:  Config object
        """
        super(NetworkDataSource, self).__init__(config)
        self.log = wireless_automation_logging.setup_logging('NetDataSource')
        self.connection = None
        self.ip_address = config['ip_address']
        self.seconds = config['seconds']
        self.port = config['port']
        self.password = config['password']
        self.fake_hardware = config['fake_hardware']
        self.iperf_server_init = config['start_iperf_server']
        self._ping_host_or_raise()
        self.connection = self._start_iperf_server_on_test_image()

    def _start_iperf_server_on_test_image(self):
        """
        Starts the iperf server. This method expects the machine
        to be running a chromeos test image. It makes assumptions
        about iperf and iptables, and the login that are true for
        chromeos test images.
        """
        if not self.iperf_server_init or self.fake_hardware:
            return None
        # SSH will open an X11 window to prompt for the password.
        os.environ['SSH_ASKPASS'] = '0'
        cmd = 'ssh -o StrictHostKeyChecking=no -o '\
              'UserKnownHostsFile=/dev/null root@%s' % self.ip_address
        self.log.debug(cmd)
        connection = pexpect.spawn(cmd, logfile=LogIt(self.log), timeout=5)
        connection.expect('(?i)password:')
        connection.sendline(self.password)
        connection.expect('#')
        self.log.info('Logging in to remote data source at %s' %
                      self.ip_address)
        self.log.info(connection.before + connection.after)
        self.log.info('running on dut: killall -9 iperf ')
        connection.sendline('killall -9 iperf')
        connection.sendline('iptables -I INPUT -p tcp --dport 5001 -j ACCEPT')
        connection.sendline('iptables -I OUTPUT -p tcp --sport 5001 -j ACCEPT')
        connection.sendline('iperf -s --port %s &' % self.port)
        try:
            connection.expect('(?i)default', timeout=1)
        except pexpect.TIMEOUT:
            self.log.error("Sending the iperf command timed out. "
                           "Not installed? ")
            raise
        self.log.info(connection.before + connection.after)
        return connection

    def _ping_host_or_raise(self):
        """
        Check to see if the iperf host is reachable.
        :return: Raises an exception if ping fails
        """
        if self.fake_hardware:
            return
        import os
        cmd = "ping -c 1 -w 2 " + self.ip_address + " > /dev/null 2>&1"
        self.log.debug(cmd)
        if self.fake_hardware:
            self.log.debug("In Fake mode, don't actually ping")
            return
        response = os.system(cmd)
        #and then check the response...
        if response == 0:
            self.log.debug('ping worked')
            return
        else:
            self.log.debug('ping failed')
            raise wireless_automation_error.ConnectionFailure(
                'iperf host is not responding to ping')

    def stop(self):
        """
        Stops the network server.
        """
        self.log.info('Stopping and disconnecting from the network data server')
        if self.fake_hardware:
            self.log('Fake stopping iperf.')
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

    @staticmethod
    def get_download_url():
        """
        Returns the URL to download from
        """
        pass

    def run_iperf_download_test(self):
        """
        Run one iperf test from the machine we are on to the remote at
        self.ip_address
        :return: A dict with the results.
        """
        if self.fake_hardware:
            self.log.info('Fake running a download test..')

        results = {"date": '121212',
                   "source_ip": self.ip_address,
                   "source_port": self.port,
                   "dest_ip": self.ip_address,
                   "dest_port": self.port,
                   "id": '1',
                   "seconds": '10',
                   "bytes": '10',
                   "bytes_per_second": '1'
                   }

        return results

        cmd = ["iperf",
               "--reportstyle", "C",
               "-c", self.ip_address,
               "--port", str(self.port)]
        self.log.info(cmd)
        iperf = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        (stdout, _) = iperf.communicate()
        stdout = stdout.rstrip()
        out = stdout.split(',')
        if len(out) < 8:
            self.log.error('iperf returned a too short result : %s ' % out)
            return None
        results = {"date": out[0],
                   "source_ip": out[1],
                   "source_port": out[2],
                   "dest_ip": out[3],
                   "dest_port": out[4],
                   "id": out[5],
                   "seconds": out[6],
                   "bytes": out[7],
                   "bytes_per_second": out[8],
                   }
        return results

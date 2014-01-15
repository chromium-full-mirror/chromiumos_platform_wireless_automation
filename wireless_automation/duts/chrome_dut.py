# Copyright (c) 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
ChromeOS Device Under Test.
"""

import subprocess

from wireless_automation.duts import dut_interface
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.aspects import wireless_automation_error
import os

from wireless_automation.utils import run_shell_command


class ChromeDut(dut_interface.DutInterface):
    """
    ChromeOS specific dut functions.
    """

    def __init__(self, config, low_level_modem_driver=None):
        dut_interface.DutInterface.__init__(self, config)
        self.log = wireless_automation_logging.setup_logging('ChromeDut')
        self.modem_driver = low_level_modem_driver
        self.fake_hardware = config['fake_hardware']

    def cellular_modem_reset(self):
        """
        Reset the cellular modem using OS level tools.
        """
        cmd = ["modem", "reset"]
        self._send_shell_command(cmd)

    def cellular_controllers_stop(self):
        """
        stop all the daemons that may talk to the modem.
        Used before controlling the modem with low level tools.
        """
        cmd = ["stop", "shill"]
        self._send_shell_command(cmd)

    def cellular_connect(self, technology='LTE'):
        """
        connect the cellular modem using OS level tools
        """
        cmd = ["modem", "connect"]
        self._send_shell_command(cmd)

    def _send_shell_command_list(self, cmds):
        for cmd in cmds:
            self.log.info(cmd)
            self._send_shell_command(cmd)

    def _send_shell_command(self, cmd):
        """
        Run a shell command on the dut
        """
        self.log.debug(cmd)
        shell_env = os.environ
        self.log.info(cmd)
        command = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   env=shell_env)
        (std_out, std_err) = command.communicate()
        self.log.debug(std_out)
        self.log.debug(std_err)

    def start_local_netperf_server(self, timeout_secs=5):
        """
        Start a local netperf server.
        This is not very robust yet, just used in some unit tests.
        :timeout: seconds
        :return:
        """
        cmd1 = ['killall', 'netserver']
        cmd2 = ['timeout', str(timeout_secs), 'netserver']
        self._send_shell_command_list([cmd1, cmd2])

    def start_local_iperf_server(self, port=5001, timeout_secs=5):
        """
        Start a local iperf server.
        This is not very robust yet, just used in some unit tests.
        :param port: port number, default=5001
        :return:
        """
        cmd1 = ['killall', '-9', 'iperf']  # -9 because iperf hangs
        cmd2 = ['timeout', str(timeout_secs), 'iperf',
                '--daemon', '-s', '--port', str(port),
                '2>/dev/null',
                '1>/dev/null', '&']
        for cmd in [cmd1, cmd2]:
            self.log.info(cmd)
            # This hangs for an unkown reason.
            #self._send_shell_command_list([cmd1, cmd2])
            # Use os.system until the CL with utils/run_shell_command lands
            os.system(' '.join(cmd))

    def parse_netperf_output(self, out_str):
        out = out_str.rstrip()
        out = out.split()
        if len(out) < 5:
            msg = ('Netperf returned a too short result : %s ' % out)
            self.log.error(msg)
            raise wireless_automation_error.BadState(msg)
        try:
            results = {"rx_socket_bytes": float(out[0]),
                       "tx_socket_bytes": float(out[1]),
                       "message_size_bytes": float(out[2]),
                       "time": float(out[3]),
                       "Mbits_sec": float(out[4]),
            }
        except ValueError:
            self.log.info('netperf results : "%s" ' % out_str)
            mesg = 'Netperf test returned non floats as values'
            self.log.error(mesg)
            raise wireless_automation_error.ConnectionFailure(mesg)
        if results['Mbits_sec'] == '0':
            mesg = ('Netperf test returned 0 bytes transferred.'
                    ' Maybe the netperf server was down?')
            self.log.error(mesg)
            raise wireless_automation_error.ConnectionFailure(mesg)
        return results

    def _check_throughput_params(self, direction):
        valid = ['uplink', 'downlink']
        if direction not in valid:
            msg = "netperf test can not run direction = '%s', only %s " % \
                  (direction, valid)
            raise wireless_automation_error.BadExternalConfig(msg)

    def run_netperf_throughput_test(self, server_ip, port=12865,
                                    transfer_seconds=10, direction='uplink'):
        """
        Run a netperf speed test.
        :param server_ip:
        :param port: port to use
        :param transfer_seconds: seconds to run the test
        :param direction:  uplink or downlink
        :return: Mega bits per second for the direction specified.
        """
        self._check_throughput_params(direction)

        if direction == 'uplink':
            netperf_test = 'TCP_STREAM'
        else:
            netperf_test = 'TCP_MAERTS'
        self._ping_host_or_raise(server_ip)

        if self.fake_hardware:
            self.log.info('Fake running a download test..')
            return 123.456

        self.log.info('Starting the download test..')
        cmd = ["netperf", server_ip,
               "-P", "0",  # Don't print any headers in the output
               "-l", str(transfer_seconds),
               "-t", str(netperf_test),
               "-p", str(port)
               ]
        self.log.info(' '.join(cmd))
        netperf = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        #  communicate() blocks until there are results
        (out_str, out_e) = netperf.communicate()
        self.log.info('netperf stderr: %s ' % out_e)
        results = self.parse_netperf_output(out_str)

        self.log.info('Netperf %s Mbps: %s' % (direction, results['Mbits_sec']))
        return results['Mbits_sec']

    def _parse_iperf_output(self, direction, out, transfer_seconds):
        out = out.rstrip()
        out = out.split(',')
        if len(out) < 8:
            mesg = 'iperf returned too short of a result : %s ' % out
            self.log.error(mesg)
            raise wireless_automation_error.ConnectionFailure(mesg)
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
        if results['bytes'] == '0':
            mesg = ('Iperf test returned 0 bytes transferred.'
                    ' Maybe the iperf server was down?')
            self.log.error(mesg)
            raise wireless_automation_error.ConnectionFailure(mesg)
        # Calc the rate. Sometimes iperf doesn't return the
        # last element in the list, but we seem to have bytes
        # and seconds all the time.
        bits_per_second = 8 * float(results['bytes']) / transfer_seconds
        mega_bits_per_seconds = bits_per_second / 1e6
        self.log.info('iperf %s Mbps: %s' % (direction, mega_bits_per_seconds))
        return mega_bits_per_seconds

    def run_iperf_throughput_test(self, iperf_server_ip, iperf_port=5001,
                                  direction='uplink', transfer_seconds=10):
        """
        Use Iperf to test throughput speeds. This expects there to be
        a iperf server running at the iperf_server_ip.
        :param iperf_server_ip: IP of the server that has iperf in server mode
        :param iperf_port: Port that iperf is using on the server
        :param bidirectional:
            How to test both direction['no','serial,'parallel' ]
        :param transfer_seconds:
        :return:
        """
        self._check_throughput_params(direction)
        self._ping_host_or_raise(iperf_server_ip)
        if self.fake_hardware:
            self.log.info('Fake running a download test..')
            return 123.456

        self.log.info('Starting the download test..')
        cmd = ["iperf",
               "--client", iperf_server_ip,
               "--reportstyle", "C",
               "--time", str(transfer_seconds),
               "--port", str(iperf_port)]
        if direction == 'downlink':
            cmd.extend(['--tradeoff'])

        self.log.info(' '.join(cmd))
        shell_cmd = run_shell_command.Command(cmd)
        shell_cmd.run(timeout=transfer_seconds + 5, shell=False)
        out = shell_cmd.output
        mega_bits_per_seconds = self._parse_iperf_output(direction,
                                                         out,
                                                         transfer_seconds)
        return mega_bits_per_seconds

    def _ping_host_or_raise(self, ip_address):
        """
        Check if the net/iperf host is reachable.
        :return: Raises an exception if ping can't connect
        """
        if self.fake_hardware:
            return
        cmd = "ping -c 1 -w 2 " + ip_address + " > /dev/null 2>&1"
        self.log.debug(cmd)
        if self.fake_hardware:
            self.log.debug("In Fake mode, don't actually ping")
            return
        response = os.system(cmd)
        #and then check the response...
        if response == 0:
            self.log.debug('ping %s worked' % ip_address)
            return
        else:
            self.log.debug('ping %s failed' % ip_address)
            raise wireless_automation_error.ConnectionFailure(
                'net/iperf host is not responding to ping: %s ' % ip_address)

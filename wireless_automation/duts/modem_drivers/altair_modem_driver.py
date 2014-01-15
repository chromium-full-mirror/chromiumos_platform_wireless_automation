# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
low level Altair modem driver
"""
import re
import subprocess

from wireless_automation.duts.modem_drivers import modem_interface

import os
import time

# The ANPTAble file before we mess with it to make the
# call box work. These are stored here to make reverting to
# to a known good state possible. They are not used in the code

APNTABLE_ORIG = """
config 'PDN' 'Class1'
option 'Class' '1'
option 'Name' 'VZWIMS'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'true'
option 'P_CSCF' '4'
option 'External' 'false'
option 'AutoRecoveryDisabled' 'false'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'

config 'PDN' 'Class2'
option 'Class' '2'
option 'Name' 'VZWADMIN'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'true'
option 'P_CSCF' '0'
option 'External' 'false'
option 'AutoRecoveryDisabled' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'

config 'PDN' 'Class3'
option 'Class' '3'
option 'Name' 'VZWINTERNET'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'true'
option 'P_CSCF' '0'
option 'External' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'
option 'AutoRecoveryDisabled' 'false'

config 'PDN' 'Class4'
option 'Class' '4'
option 'Name' 'VZWAPP'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'false'
option 'P_CSCF' '0'
option 'External' 'false'
option 'AutoRecoveryDisabled' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'

config 'PDN' 'Class5'
option 'Class' '5'
option 'Name' 'INTERNET'
option 'IP_Type' 'IP'
option 'Enabled' 'true'
option 'P_CSCF' '0'
option 'External' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'
option 'AutoRecoveryDisabled' 'false'

"""

# The PXT connects with this APN file.
APNTABLE_FOR_CONNECTING_TO_PXT = """
config 'PDN' 'Class1'
option 'Class' '1'
option 'Name' 'VZWIMS'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'true'
option 'P_CSCF' '4'
option 'External' 'false'
option 'AutoRecoveryDisabled' 'false'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'

config 'PDN' 'Class2'
option 'Class' '2'
option 'Name' 'VZWADMIN'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'true'
option 'P_CSCF' '0'
option 'External' 'false'
option 'AutoRecoveryDisabled' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'

config 'PDN' 'Class3'
option 'Class' '3'
option 'Name' 'VZWINTERNET'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'true'
option 'P_CSCF' '0'
option 'External' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'
option 'AutoRecoveryDisabled' 'false'

config 'PDN' 'Class4'
option 'Class' '4'
option 'Name' 'VZWAPP'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'false'
option 'P_CSCF' '0'
option 'External' 'false'
option 'AutoRecoveryDisabled' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'

config 'PDN' 'Class5'
option 'Class' '5'
option 'Name' 'INTERNET'
option 'IP_Type' 'IP'
option 'Enabled' 'true'
option 'P_CSCF' '0'
option 'External' 'true'
option 'PcoId' 'null'
option 'PcoPayload' 'null'
option 'AuthType' 'null'
option 'AuthName' 'null'
option 'AuthPwd' 'null'
option 'AuthHostname' 'null'
option 'AutoRecoveryDisabled' 'false'

"""

# This apntable is used if at%setacfg=ecm.Mode.VzwImsTestMode is true
APNTABLE_VZW_IMSTEST = """

config 'PDN' 'Class1'
option 'Class' '1'
option 'IP_Type' 'IPV4V6'
option 'Enabled' 'true'
option 'P_CSCF' '0'
option 'External' 'true'
option 'External_vlan_id' '0'
option 'AutoRecoveryDisabled' 'false'
option 'Name' 'internet'

"""

# This file points to the apntable_vzw_imstest file
ECM = ("\n"
       "config 'Environment' 'Config'\n"
       "\toption 'OutputSocketFile' '/tmp/atsw3'\n"
       "\toption 'InputSocketFile' '/tmp/ecm'\n"
       "\toption 'HookDir' '/etc/ecm'\n"
       "\n"
       "config 'Global' 'Mode'\n"
       "\toption 'EchoMode' 'true'\n"
       "\toption 'VzwMode' 'true'\n"
       "\toption 'LabMode' 'true'\n"
       "\toption 'AutoConnectMode' 'true'\n"
       "\toption 'CatIgnoreMode' 'false'\n"
       "\toption 'RecoveryDisableMode' 'false'\n"
       "\toption 'VzwImsTestMode' 'true'\n"
       "\toption 'ImsRegBypassMode' 'true'\n"
       "\n"
       "config 'Environment' 'PDN'\n"
       "\toption 'PredefinedPDNMask' '0'\n"
       "\toption 'InternalImsClass' '1'\n"
       "\toption 'AdminClass' '2'\n"
       "\toption 'DataClass2' '4'\n"
       "\toption 'DataClass1' '1'\n"
       "\n"
       "config 'Environment' 'Timeout'\n"
       "\toption 'IoResponse' '60000'\n"
       "\toption 'EstablishedInterface' '30000'\n"
       "\toption 'ImsRegistration' '60000'\n"
       "\toption 'MonitorPollingShort' '200'\n"
       "\toption 'MonitorPollingRegular' '1500'\n"
       "\toption 'CmdResponsePolling' '100'\n"
       "\toption 'PhyDelay' '0'\n"
       "\n"
       "config 'Recovery' 'ModemRecovery'\n"
       "\toption 'EnableReboot' 'false'\n"
       "\toption 'CollectLogs' 'false'\n"
       "\toption 'AtChMonInterval' '0'\n"
       "\toption 'AtFailRecThr' '5'\n"
       "\n"
       "config 'LabMode' 'VzwImsTestMode'\n"
       "\toption 'APNTableFile' 'apntable-vzw-imstest'\n"
       "\n"
       )


class AltairModem(modem_interface.ModemInterface):
    """
    The Altair specific implementation
    """
    CONFIGSPEC = ['serial_file=string(default=/dev/ttyACM0)']

    def __init__(self, l_config):
        modem_interface.ModemInterface.__init__(self, l_config)

    def is_modem_there(self):
        return True

    def reset(self):
        self._run_at_command('atz')

    def hard_power_cycle(self, block=True):
        os.system('/usr/sbin/ectool i2cwrite 8 0 0x90 0x11 0xe')
        time.sleep(1)
        os.system('/usr/sbin/ectool i2cwrite 8 0 0x90 0x11 0x1f')
        device_name_re = '.*:0047.*'
        for i in range(20):
            time.sleep(1)
            devices = subprocess.check_output('lsusb', shell=True)
            self.log.debug('wating for %s to appear in lsusb..' %
                           device_name_re)
            if re.search(device_name_re, devices, re.MULTILINE):
                return

        self.log.error(devices)
        raise SystemError('Modem did not appear with lsusb ')

    def airplane_mode_off(self):
        self._run_at_command('at%cfun=1')

    def airplane_mode_on(self):
        self._run_at_command('at%cmatt=0')  # Detatch from network first.
        self._run_at_command('at%cfun=0')

    def register(self):
        raise NotImplementedError

    def is_registered(self):
        raise NotImplementedError

    def deregister(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def is_connected(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def prepare_to_send_data(self):
        raise NotImplementedError

    def is_ready_to_send_data(self):
        raise NotImplementedError

    def get_signal_strength(self):
        raise NotImplementedError

    def setup_for_call_box(self):
        self._run_at_command('at%setacfg=ecm.PDN.DataClass1,1')
        self._run_at_command('at%setacfg=ecm.Mode.VzwImsTestMode,true')
        self._run_at_command('at%setacfg=ecm.Mode.'
                             'ImsRegBypassMode,true')
        self._run_at_command('at%setacfg=APNTable.'
                             'Class3.AutoRecoveryDisabled,false')
        self._run_at_command('at%setacfg=APNTable.'
                             'Class5.AutoRecoveryDisabled,false')

    def get_version_string(self):
        """
        Return the version
        """
        return self._run_at_command('at%ver')

    def set_ip(self):
        """
        Configure the right eth interface to ssh to the modem.
        :return:
        """
        cmd = ("x=`ifconfig -a | "
               "grep '^eth[0-9].*08:9e:01:' |"
               " cut -d ' ' -f 1`;"
               "ifconfig $x 10.0.0.10")
        self._run_shell_script(cmd)

    def _run_shell_script(self, script_string):
        """
        Run a string as a bash shell script.
        :param script_string:
        :return: output of script
        """
        self.log.debug('Shell : %s ' % script_string)
        ret_val = subprocess.check_output(script_string, shell=True)
        self.log.debug('Shell Response: %s ' % ret_val)
        return ret_val

    def _run_at_command(self, at_command):
        """
        Run an AT command on the modem.
        :param at_command: command to run.
        :return: the text result.
        """
        cmd = ("(echo '%s' && exec sleep 2 )  | "
               "socat /dev/ttyACM0,nonblock,crnl,echo=0 stdio" % at_command)

        self.log.debug(cmd)
        self.log.debug('Sending AT Command : %s ' % at_command)
        ret_val = subprocess.check_output(cmd, shell=True)
        self.log.debug('AT Response: %s ' % ret_val)
        return ret_val


if __name__ == "__main__":
    # pylint: disable=invalid-name
    config = AltairModem.get_default_config()
    modem_driver = AltairModem(config)
    modem_driver.hard_power_cycle()
    #modem_driver.set_ip()
    modem_driver.get_version_string()
    modem_driver.airplane_mode_on()
    modem_driver.airplane_mode_off()
    modem_driver.setup_for_call_box()

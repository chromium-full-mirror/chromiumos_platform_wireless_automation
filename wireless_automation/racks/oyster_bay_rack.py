# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The OysterBayRack details. Derived from CallBoxRackInterface.
"""

from wireless_automation.aspects import configurable
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.duts import dut_factory
from wireless_automation.instruments.call_box import call_box_factory
from wireless_automation.instruments import rf_switch
from wireless_automation.instruments.network_data_source \
    import network_data_source
from wireless_automation.racks import call_box_rack_interface
# OysterBayPxtDevelopmentRack looks abstract. TODO(byronk): do we need methods?
# pylint: disable=interface-not-implemented


class OysterBayPxtDevelopmentRack(call_box_rack_interface.CallBoxRackInterface):
    """
    Representation of the development rack in OysterBay.
    """
    # CONFIGSPEC is inherited from CallBoxRackInterface, and the configspec
    # is part of that. Default values can change, but
    # changing entries suggests you don't want a derived class.
    base_configspec = call_box_rack_interface.CallBoxRackInterface.CONFIGSPEC
    base_configspec = configurable.list_to_configspec(base_configspec)
    # Change the IP's to the right ones for this lab
    base_configspec['CallBoxFactory']['CallBox']['scpi_ip_address'] = \
        "ip_addr(default='172.22.50.244')"
    base_configspec['RfSwitch']['ip_address'] = \
        "ip_addr(default='172.22.50.244')"
    CONFIGSPEC = base_configspec

    def __init__(self, config):
        super(OysterBayPxtDevelopmentRack, self).__init__(config)
        self.log = wireless_automation_logging.setup_logging('Rack')

        cbf_config = config['CallBoxFactory']
        self.call_box = call_box_factory.build_one(cbf_config)

        rfs_config = config['RfSwitch']
        self.rf_switch = rf_switch.RfSwitch(rfs_config)

        dut_config = config['Dut']
        self.dut = dut_factory.build_one(dut_config)

        cd_config = config['NetworkDataSource']
        self.network_data_source = network_data_source.NetworkDataSource(cd_config)

    def reset(self):
        """
        Reset entire rack.
        """
        self.call_box.reset()


class ChromebookInfo(object):  # pylint:disable=too-many-instance-attributes,too-few-public-methods,line-too-long
    """
    A class to store Chromebook info.
    todo(byronk): This class should be in a separate file? But the data
    is only useful for OysterBayRack.
    Fix this when we have a better idea what the job of a rack is.
    So all these pylint disables can go away.
    """
    def __init__(self, name, ip, mac, modem,  # pylint:disable=too-many-arguments,line-too-long
                 air_interfaces, location, rfswitch, switch_port):
        self.long_name = name  # Long and meaningful name.
        self.gpib_ip = ip  # The IP address of the GPIB bus.
        self.mac = mac  # Hardware MAC address of the Ethernet interface
        self.modem = modem  # The name of the modem
        #assert air_interfaces in all_air_interfaces
        self.air_interfaces = air_interfaces
        self.location = location
        self.rf_switch = rfswitch
        self.switch_port = switch_port

LAB_CHROMEBOOK_DICT = {
    'link-lte': ChromebookInfo(name='DVT Link with LTE',
                               ip="172.22.50.86",
                               mac="00:0e:c6:89:9d:18",
                               modem='GOBI3K',
                               air_interfaces=["LTE"],
                               location="rack2-host6",
                               rfswitch="switch_1",
                               switch_port="port1")
}

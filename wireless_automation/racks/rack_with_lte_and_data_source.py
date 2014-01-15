# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
The OysterBayRack details. Derived from CallBoxRackInterface.
"""

from wireless_automation.aspects import configurable
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.instruments.call_box import call_box_interface
from wireless_automation.instruments.call_box.agilent_pxt import call_box_pxt
from wireless_automation.instruments.network_data_source \
    import network_data_source

# This class looks abstract because it doesn't have any functions.
# It's used here as a container class, to hold both the parts of
# rack, as well as the knowledge of how to setup that rack.
# pylint: disable=interface-not-implemented


class RackWithLteAndDataSourceBase(configurable.Configurable):
    """
    Representation of the development rack in OysterBay.
    This does not contain a DUT.  DUTs are connected to
    the rack for tests.
    """
    CONFIGSPEC = [
        'reset_everything = boolean(default=True)'] +\
        configurable.nest_configspecs([
            ('LteCallBox', call_box_interface.CallBoxLteInterface),
            ('NetworkDataSource', network_data_source.NetworkDataSource)
        ])

    def __init__(self, config):
        """
        :type self: object
        """
        super(RackWithLteAndDataSourceBase, self).__init__(config)
        self.log = wireless_automation_logging.setup_logging('Rack')
        self.log.info('Constructing : %s' % self.__class__)

        cd_config = config['NetworkDataSource']
        self.network_data_source = (
            network_data_source.NetworkDataSource(cd_config))

    def reset(self):
        """
        Reset entire rack.
        """
        # todo: add rest of parts to reset here
# pylint: enable=interface-not-implemented


class OysterBayPxtDevelopmentRack(RackWithLteAndDataSourceBase):
    """
    Specific settings for the specific rack in Oyster Bay.
    This is a good place to set IP addresses.
    """
    # Change the config settings for OysterBay
    base_configspec = RackWithLteAndDataSourceBase.CONFIGSPEC
    CONFIGSPEC = configurable.list_to_configspec(base_configspec)
    # Change the IP's to the right ones for this lab
    CONFIGSPEC['LteCallBox']['scpi_ip_address'] = \
        "ip_addr(default='172.22.50.236')"
    CONFIGSPEC['NetworkDataSource']['ssh_ip_address'] = \
        "ip_addr(default='172.22.50.236')"
    CONFIGSPEC['NetworkDataSource']['ssh_port'] = 'integer(default=222)'

    def __init__(self, config):
        RackWithLteAndDataSourceBase.__init__(self, config)
        self.log.info('Constructing : %s' % self.__class__)
        cbf_config = config['LteCallBox']
        self.call_box = call_box_pxt.CallBoxPxt(cbf_config)
        assert True


class RackWithLteAndHspa3GAndDataSourceBase(RackWithLteAndDataSourceBase):
    """
    Abstract class that adds the HSPA and 3G ability to the LTE Rack.
    """
    base_configspec = RackWithLteAndDataSourceBase.CONFIGSPEC
    CONFIGSPEC = configurable.list_to_configspec(base_configspec)

    def __init__(self, config):
        RackWithLteAndDataSourceBase.__init__(self, config)
        self.log.info('Constructing : %s' % self.__class__)

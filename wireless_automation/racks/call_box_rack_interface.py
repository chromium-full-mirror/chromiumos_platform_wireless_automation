# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Definition of base racks. These define all the high level types
of racks which tests use. There is one Rack Base for each major type
of equipment setup; e.g. the PowerConsumptionRackBase, the
CellularCallBoxRackBase, the CellularFemtocellRackBase. The specifics
are handled by the children. CellularCallBoxRackBase may have

Building1CellularCallBoxRack
Building2CellularCallBoxRack

With each of these containing the knowledge of how that particular
lab is wired up. The RF ports may go through a splitter,  a notch
filter and a series of RF switches. All this goes in this child
class and the all the tests that use this rack never have to care.

"""

from wireless_automation.aspects import configurable
from wireless_automation.duts import dut_factory
from wireless_automation.instruments.call_box import call_box_factory
from wireless_automation.instruments.network_data_source \
    import network_data_source
from wireless_automation.instruments.rf_switch import RfSwitch


class CallBoxRackInterface(configurable.Configurable):
    """
    Base class for call box racks. Tests should be able to
    run with any CallBoxRack.

    """
    CONFIGSPEC = [
        'reset_everything = boolean(default=True)'] +\
        configurable.nest_configspecs([
            ('CallBoxFactory', call_box_factory.CallBoxFactory),
            ('RfSwitch', RfSwitch),
            ('Dut', dut_factory.DutFactory),
            ('NetworkDataSource', network_data_source.NetworkDataSource)
        ])

    def __init__(self, config):
        super(CallBoxRackInterface, self).__init__(config)

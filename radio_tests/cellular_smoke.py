# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

#Example code to for the autotest stub that will call this file.

#from wireless_automation.aspects.measurement_list import the_measurement_list

# class cellular_smoke(test.test):
#     # The autotest infrastructure calls run_once.  The control file
#     def run_once(self):
#         cellular_smoke()
#         print the_measurement_list

from wireless_automation.aspects import configurable
from wireless_automation.aspects.measurement_list import TheMeasurementList
from wireless_automation.racks import oyster_bay_rack


class CellularSmoke(configurable.Configurable):
    CONFIGSPEC = ["config_stuff=string(default='CellularSmokeConfig')"]

    def __init__(self, config):
        super(CellularSmoke, self).__init__(config)
        config = oyster_bay_rack.\
            OysterBayPxtDevelopmentRack.get_default_config()
        config['call_box']['use_fake'] = True
        self.rack = oyster_bay_rack.OysterBayPxtDevelopmentRack(config)

    def run(self):
        """
        From Requirement:
        Description:

        @return:
        """
        # Arrange
        self.rack.call_box.start()
        self.rack.network_data_source.start()
        self.rack.chrome_device.modem.connect()

        # Act
        url = self.rack.network_data_source.get_download_url()
        speed = self.rack.chrome_device.measure_download_speed(url)

        # Assert
        assert speed > 0

        # Record
        TheMeasurementList.append(name='download_speed', value=speed)

        # Annihilate or Reset
        # Done implicitly via the destructors



def run(channel, dut_name, pxt_ip):
    config = CellularSmoke.get_default_config()
    config['channel'] = channel
    cellular_smoke = CellularSmoke(config)
    cellular_smoke.run()


if __name__ == "__main__":
    import sys
    config = sys.argv[1]
    run(config)


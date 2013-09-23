# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import logging
import sys
from wireless_automation.aspects.wireless_automation_logging import \
    setup_logging
from wireless_automation.instruments.call_box.agilent_pxt import call_box_pxt

log = setup_logging('change power', level=logging.CRITICAL)
prologix_logger = setup_logging('prologix', level=logging.CRITICAL)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print "Only provide one paramater on the command line "
        exit()
    power = sys.argv[1]
    assert float(power)
    config = call_box_pxt.CallBoxPxt.get_default_config()
    pxt = call_box_pxt.CallBoxPxt(config)
    pxt.set_power_dbm(power)


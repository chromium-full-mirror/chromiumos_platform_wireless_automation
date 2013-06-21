# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os
import time
from wireless_automation.aspects.configurable import Configurable
from wireless_automation.aspects.wireless_automation_logging import \
    setup_logging

log = setup_logging('AltairModem')

class AltairLteModem(Configurable):
    """

    """
    def __init__(self):
        """
        @return:
        """
        pass

    def power_cycle(self):
        """

        @return:
        """
        power_down_str = 'ectool i2cwrite 8 0 0x90 0x11 0xe'
        power_up_str = 'ectool i2cwrite 8 0 0x90 0x11 0x1f'

        log.info('Writing : %s' % power_down_str)
        os.system(power_down_str)

        log.info('sleeping for 5 seconds...')
        time.sleep(5)

        log.info('Writing : %s' % power_up_str)
        os.system(power_up_str)

# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from wireless_automation.instruments.call_box.agilent_pxt import Pxt
from wireless_automation.chrome_device.modems import modem_base

if __main__ == 'main':
    config = Pxt.get_default_config()
    pxt = Pxt(config)
    modem = modem_base()

    modem.start()
    pxt.start()


# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from wireless_automation.aspects.configurable import Configurable
from wireless_automation.chrome_device.modems import modem_base


class ChromeDevice (Configurable):
    """
    TODO:
    A place holder, this class should return an object composed
    of all the objected needed to talk to the chromebook systems:
    shill, modemmanger, the modem direct, open and close switch,
    power reporting, etc.
    """
    configspec = ["modem = string(default='gobi3000') "]

    def __init__(self):
        pass
        #self.modem = modem_base.ModemBase

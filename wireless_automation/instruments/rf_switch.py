# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Control of a RF switch
"""
from wireless_automation.aspects import configurable


class RfSwitch(configurable.Configurable):
    """
    Control of a RF Switch.
    """
    CONFIGSPEC = ['ip_address=ip_addr(default="0.0.0.0")',
                  'port=integer(default=0)',
                  'position=integer(default=0)'
                  ]

    def __init__(self, config):
        super(RfSwitch, self).__init__(config)

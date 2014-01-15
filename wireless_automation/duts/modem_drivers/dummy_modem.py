# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
A dummy modem class, to provide modem functionality on workstations that
have no modems.
"""

from wireless_automation.duts.modem_drivers import modem_interface


class DummyModem(modem_interface.ModemInterface):
    """
    A dummy modem class.

    """

    def __init__(self, config):
        """
        @param config: a Config object.
        """
        super(DummyModem, self).__init__(config)

    def is_modem_there(self):
        return True

    def reset(self):
        pass

    def hard_power_cycle(self, block=True):
        pass

    def airplane_mode_on(self):
        pass

    def airplane_mode_off(self):
        pass

    def register(self):
        pass

    def is_registered(self):
        return True

    def deregister(self):
        pass

    def connect(self):
        pass

    def is_connected(self):
        return True

    def disconnect(self):
        pass

    def prepare_to_send_data(self):
        pass

    def is_ready_to_send_data(self):
        return True

    def get_signal_strength(self):
        return -77

    def setup_for_call_box(self):
        pass

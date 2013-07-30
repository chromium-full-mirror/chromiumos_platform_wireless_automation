# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import functools
from instruments.call_box import call_box_interface
from wireless_automation.aspects import wireless_automation_error
from wireless_automation.aspects import wireless_automation_logging
from wireless_automation.instruments.call_box.agilent_pxt \
        import call_box_pxt

log = wireless_automation_logging.setup_logging('call_box_fake')


def log_args_and_return_values(f):
    """
    Logs each call, with the name of the function, the input args, and
    the return values. This produces similar output to the real PXT.
    """
    @functools.wraps(f)  # To preserve the metadata of the wrapped functions
    def _inner(*args, **kwargs):
        args_str = str(args[1:])  # First arg is class name. Not useful.
        args_str += str(kwargs)
        log.info('called : %s() ' % f.__name__)
        log.debug('called : %s() with %s ' % (f.__name__, args_str))
        ret_val = f(*args, **kwargs)
        log.info('returned : %s' % ret_val)
        return ret_val
    return _inner


class CallBoxFakeBase(call_box_interface.CallBoxInterface):
    # These are empty because this is a base class.
    ALL_STATES = []              # List of possible states
    IDLE_STATES = []             # The state that means it's idle
    CONNECTED_STATES = []        # The states that count as connected
    IDN_STRING = "*idn? return"  # The ID string *IDN? returns

    @log_args_and_return_values
    def __init__(self, config):
        super(CallBoxFakeBase, self).__init__(config)
        self._power = None
        self._rf_on = None
        self.reset()

    def get_id(self):
        return self.IDN_STRING

    @log_args_and_return_values
    def reset(self):
        self._current_state = self.ALL_STATES[0]
        self._power = -99    # Current power, dBm
        self._rf_on = False

    @log_args_and_return_values
    def is_idle(self):
        return self._current_state in self.IDLE_STATES

    @log_args_and_return_values
    def close(self):
        pass

    @log_args_and_return_values
    def is_connected(self):
        log.debug('in state: %s ' % self._current_state)
        return self._current_state in self.CONNECTED_STATES

    @log_args_and_return_values
    def _get_cell_status(self):
        return self._current_state

    @log_args_and_return_values
    def set_power_dbm(self, dbm):
        if not -120 < dbm < 40:
            raise wireless_automation_error.BadScpiCommand(
                'FakePXT Power Level was set out of range %s' % dbm)
        self._power = dbm

    @log_args_and_return_values
    def get_power_dbm(self):
        return float(self._power)

    @log_args_and_return_values
    def is_rf_on(self):
        return self._rf_on

    @log_args_and_return_values
    def turn_rf_on(self):
        self._rf_on = True

    @log_args_and_return_values
    def turn_rf_off(self):
        self._rf_on = False

    @log_args_and_return_values
    def start(self):
        self._current_state = self.CONNECTED_STATES[0]

    @log_args_and_return_values
    def stop(self):
        self._current_state = self.IDLE_STATES[0]


class CallBoxPxt(CallBoxFakeBase):
    """
    Map the real PXT values, so we test those.
    """
    CONFIGSPEC = call_box_pxt.CallBoxPxt.CONFIGSPEC
    ALL_STATES = call_box_pxt.CallBoxPxt.ALL_STATES
    CONNECTED_STATES = call_box_pxt.CallBoxPxt.CONNECTED_STATES
    IDLE_STATES = call_box_pxt.CallBoxPxt.IDLE_STATES
    IDN_STRING = call_box_pxt.CallBoxPxt.IDN_STRING
    MATCH_IN_ID_STRING = call_box_pxt.CallBoxPxt.MATCH_IN_ID_STRING

    def __init__(self, config):
        super(CallBoxPxt, self).__init__(config)
        self._current_call_state = 0
        self._power = None

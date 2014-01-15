# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
Base class for all modems.
"""

from wireless_automation.aspects import configurable


class ModemInterface(configurable.Configurable):
    """
    A base class for controlling the modem.
    The flow for these states:

        if self.is_modem_there():
            self.reset()
        else:
            modem.hard_power_cycle()
            self.reset()
        modem.setup_for_call_box()
        modem.register()
        modem.connect()
        modem.prepare_to_send_data()
        if modem.is_ready_to_send_data()
            dut.download_url()
            rsi = modem.get_signal_strength()
        modem.disconnect()
        assert not modem.is_connected()
        modem.airplane_mode_on()

    """
    CONFIGSPEC = ['']

    def __init__(self, config):
        """
        :param config: Config object.
        """
        super(ModemInterface, self).__init__(config)

    def is_modem_there(self):
        """
        Can the modem be reached. If the modem is off or
        non responsive, returns a False.
        :return: Boolean.
        """
        raise NotImplementedError

    def reset(self):
        """
        Takes a modem that is responsive, and resets it's state such
        that it's ready for a new test or new connection. All the state
        from before is erased. This should be similar in effect to
        a hard power cycle, but faster.
        """
        raise NotImplementedError

    def hard_power_cycle(self, block=True):
        """
        Powers off the modem by killing the power lines to it.
        Or as close to that as possible. This should be a
        the hardest reset available.
        Then powers the modem back up. This blocks until
        the modem is responsive.

        :block: return only after the modem responsive
        """
        raise NotImplementedError

    def airplane_mode_off(self):
        """
        Take a powered modem and prepare it to connect.
        Example: at+cfun=1
        """
        raise NotImplementedError

    def airplane_mode_on(self):
        """
        Put the modem into a state that is: powered, not connected,
        and not responding to the base station. This is not a 'sleep'
        or 'low power' mode.
        Example: at+cfun=0
        """
        raise NotImplementedError

    def register(self):
        """
        Register with the network.
        """
        raise NotImplementedError

    def is_registered(self):
        """
        Is the modem registered with the cellular network.
        If registered, should be able to connect.
        :return: Boolean.
        """
        raise NotImplementedError

    def deregister(self):
        """
        Deregister with the network.
        """
        raise NotImplementedError

    def connect(self):
        """
        Connect
        """
        raise NotImplementedError

    def is_connected(self):
        """
        Is the modem 'connected' to the base station.
        :return:
        """
        raise NotImplementedError

    def disconnect(self):
        """
        Disconnect from the network.
        """
        raise NotImplementedError

    def prepare_to_send_data(self):
        """
        Register, Connect, setup any IP and routing tables
        that are needed to get data to f"low over the
        cellular network.
        :return: Boolean
        """
        raise NotImplementedError

    def is_ready_to_send_data(self):
        """
        The modem is ready to start sending data.
        :return:
        """

    def get_signal_strength(self):
        """
        Get the received signal strength
        :return: Signal Strength in dBm.
        """
        raise NotImplementedError

    def setup_for_call_box(self):
        """
        Configs the modem to talk a call box
        """
        raise NotImplementedError

    def get_version_string(self):
        """
        :return: return the modem version string.
        """

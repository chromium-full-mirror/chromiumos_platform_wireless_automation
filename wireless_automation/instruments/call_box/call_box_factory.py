# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""
A factory to build the correct call_box given a config.
This only works for functionality that can be polymorphic. So any
tests that need to use features that are specific to one call box
should instantiate that call box directly and not use this factory.
"""

from wireless_automation.aspects import configurable
from wireless_automation.instruments.call_box import call_box_interface
from wireless_automation.instruments.call_box.agilent_pxt import call_box_pxt
from wireless_automation.instruments.call_box import call_box_fake


class CallBoxFactory(configurable.Configurable):
    """
    Generate a call box factory with a config
    >>> config = CallBoxFactory.get_default_config()
    >>> call_box_factory = CallBoxFactory(config)
    >>> call_box = call_box_factory.builder()

    """
    CONFIGSPEC = \
        ['call_box_model=option("pxt","8960","fake", default="fake")'] + \
        configurable.nest_configspecs([
            ('CallBox', call_box_interface.CallBoxInterface)
        ])

    def __init__(self, config):
        super(CallBoxFactory, self).__init__(config)
        self.config = config

    def builder(self):
        """
        Return one call box object.
        """
        model = self.config['call_box_model']
        call_box_config = self.config['CallBox']
        if model == 'pxt':
            return call_box_pxt.CallBoxPxt(call_box_config)
        if model == 'fake':
            return call_box_fake.CallBoxFakePxt(call_box_config)

    @classmethod
    def build_one(cls, config):
        """
        Returns one callbox, built to the incoming config
        :param config: Config
        :return: a CallBox that implements CallBoxInterface
        """
        factory = CallBoxFactory(config)
        return factory.builder()

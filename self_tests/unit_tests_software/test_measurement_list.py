# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import unittest

from wireless_automation.aspects import measurement_list


class test_measurement_list(unittest.TestCase):
    """
    Test the list
    """
    def setUp(self):
        self.the_list = measurement_list.TheMeasurementList

    def tearDown(self):
        self.the_list.delete_contents()

    def test_make_one(self):
        # setUp and tearDown get called.
        pass

    def test_make_two_and_they_are_the_same(self):
        m = measurement_list.TheMeasurementList
        mm = measurement_list.TheMeasurementList
        assert m is mm

    def test_add_one_value(self):
        self.the_list.append(name='name_here', value='value_here')
        assert len(self.the_list._global_measurement_list) == 1
        assert self.the_list._global_measurement_list[0].name == 'name_here'
        assert self.the_list._global_measurement_list[0].value == 'value_here'

    def test_to_string(self):
        self.the_list.append(name='name_here', value='value_here')
        self.the_list.append(name='name_here2', value='value_here2')
        answer = "name_here,value_here\n" + "name_here2,value_here2"
        assert str(self.the_list) == answer

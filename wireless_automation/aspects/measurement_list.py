# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""
A 'global' repository for measurements. When something worth remembering,
(boot time, how long init takes on a test instrument) it gets saved here.

This is a first pass of what this should look like. Feel free to improve it.
"""

import time


class Measurement(object):
    # disable to few public methods
    # pylint: disable=R0903
    """
    Holds all the bits about one measurement
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.time = time.ctime()

    def __str__(self):
        return "%s,%s" % (self.name, self.value)


class MeasurementList(object):
    """
    Holds a list of Measurements
    """
    _global_measurement_list = []

    def __init__(self):
        pass

    def append(self, name, value):
        """
        @param name: The name of the parameter to save.
        @param value:  The value.
        @return: None
        """
        measurement = Measurement(name=name, value=value)
        self._global_measurement_list.append(measurement)

    def delete_contents(self):
        """
        Removes all previously saved measurements from this list.
        @return:
        """
        del self._global_measurement_list[:]

    def __str__(self):
        str_list = [str(x) for x in self._global_measurement_list]
        return "\n".join(str_list)


TheMeasurementList = MeasurementList()  # pylint: disable=invalid-name

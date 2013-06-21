#!/usr/bin/python
# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# TODO(byronk): Consider using /autotest/files/utils/unittest_suite.py
# instead of this test runner.

import unittest
import logging
import sys
# To run this inside the wireless_automation dir, we have to add .. to
# the path so we can load wireless_automation
from optparse import OptionParser


def main(argv):
    parser = OptionParser()
    parser.add_option("-n", "--with-hardware", dest="with_hardware",
                      action="store_true", default=False,
                      help="Normally fakes are used. This tests against"
                      "real hardware")
    parser.add_option("-l", "--with_logs",
                      action="store_true", dest="with_logs", default=False,
                      help="print log messages to stdout")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print log messages to stdout")
    parser.add_option('-d', '--test_dir', dest='test_dir', default='.',
                      help='Recursively run tests under this dir ')

    (options, args) = parser.parse_args(argv)
    if not options.with_logs:
        print 'Disabling all loggers....'
        # Disable all loggers to make the test output easier to read.
        logging.disable(100)

    # _with_hardware is used in test file names when they need actual hardware.
    test_files_pattern = '*_test*.py'
    if not options.with_hardware:
        # Sub in software stubs if we run with no hardware
        # TODO(byronk): Move this to the factory, after the factory is written
        sys.modules['call_box_pxt'] = call_box_fake
        test_files_pattern = '*_test.py'

    verbosity = 2
    if options.verbose:
        print 'Setting verbosity to 3'
        verbosity = 3

    test_loader = unittest.defaultTestLoader.discover(
            options.test_dir,
            pattern=test_files_pattern)
    test_runner = unittest.TextTestRunner(verbosity=verbosity, buffer=True)
    test_runner.run(test_loader)

if __name__ == '__main__':
    # Munge the path so we can run this file from inside the wireless_automation
    # dir, rather then having to cd .. and then run it. Do it here to avoid
    # any global path munging that would affect a file that imported this file.
    # All wireless_automation imports have to come below this path change.
    sys.path.append('..')
    from wireless_automation.instruments.call_box.agilent_pxt import \
            call_box_fake
    main(sys.argv)
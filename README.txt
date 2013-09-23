:Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
:Use of this source code is governed by a BSD-style license that can be
:found in the LICENSE file.

=====================
Wireless Automation
=====================

***************
Goal
***************

A reusable library to automate wireless testing:

* Test instrument control
    * Call box emulators
    * DC power meters
    * RF switches

* DUT control:
    * Chromebooks
    * Modems
    * Screen brightness
    * Networking stack control


************************
Style Guide
************************

pep8.py and pylint define the style. If these tools pass the code, then the code passes.
Of note, 80 char line length is used, expect for when a pylint disable directive is used,
then longer lines are ok::

    from some.where.over.the.rainbow.way.out.there import a_wicked_witch # pylint: disable:ignore-missing-witch,ignore-long-line

The alternative is to add a a line before and a line after::

    # pylint : disable=ignore-missing-witch
    from some.where.over.the.rainbow.way.out.there import a_wicked_witch
    # pylint : enable=ignore-missing-witch

Both are acceptable. Use the right one at the right time.




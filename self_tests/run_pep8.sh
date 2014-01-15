#!/bin/sh
# Copyright (c) 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Ignore E121, line indents are not multiples of 4 spaces. This breaks
# lining up a split line to the (, unless that ( is a multiple of 4
# characters into the line.

# The validate.py and configobj.py files are external projects. They
# are just copied here. A better way may be to add
# configobj==4.7.
# to the requirements.txt file and remove them from wireless_automation

# Ignore line length here, and have pylint do that checking.

pep8 --exclude=validate.py,configobj.py \
     --ignore=E501,E121 \
     ../wireless_automation

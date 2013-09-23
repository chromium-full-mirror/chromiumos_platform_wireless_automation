# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
import os
os.system('stop modemmanager')
os.system('ModemManager --debug --log-file=/tmp/modem_manager.log&')

# Or, enable without
#os.system('modem set-logging debug')

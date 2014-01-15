#!/usr/bin/python
# Copyright (c) 2014 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

scpi_instruments = {
    # Agilent 8960 call box
    "8960": {'name': '8960', 'gpib_addr': '14',
             'ip': '172.22.50.236', 'port': 1235},
    # PXT is called 6621
    "pxt": {'name': '6621', 'gpib_addr': '14',
            'ip': '172.22.50.236', 'port': 1234}
}

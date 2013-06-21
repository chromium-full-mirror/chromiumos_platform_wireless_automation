# Copyright (c) 2013 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This is an overview of the file structure, in this
# text file for easy reading :

wireless_automation
├── aspects
│   ├── configurable.py
│   ├── cellular_system_error.py
│   ├── wireless_automation_error.py
│   └── wireless_automation_logging.py
├── chrome_device
│   ├── __init__.py
│   ├── mm1-placeholer.py
│   ├── modem1-placeholder.py
│   ├── modems
│   │   ├── altair.py
│   │   ├── gobi3k.py
│   │   ├── __init__.py
│   │   ├── modem_base.py
│   │   ├── modem_factory.py
│   │   ├── psudomodem
│   │   │   └── __init__.py
│   │   └── ward_modem
│   │       └── __init__.py
│   ├── power_supply
│   │   └── __init__.py
│   └── wifi
│       └── __init__.py
├── __init__.py
├── instruments
│   ├── call_box
│   │   ├── agilent_pxt
│   │   │   ├── call_box_fake.py
│   │   │   ├── call_box_fake_test.py
│   │   │   ├── call_box_interface.py
│   │   │   ├── call_box_pxt.py
│   │   │   ├── call_box_pxt_test_with_hardware.py
│   │   │   └── __init__.py
│   │   └── call_box_factory.py
│   ├── __init__.py
│   └── prologix
│       ├── __init__.py
│       ├── prologix_scpi_driver.py
│       └── prologix_scpi_driver_test_with_hardware.py
├── labs
│   ├── __init__.py
│   └── labconfig_data.py
├── README.txt
├── requirements
│   ├── carrier_engineering_requirements.txt
│   ├── product_engineering_requirements.txt
│   └── rf_performance_requirements.txt
├── run_all_tests.py
└── setup.py

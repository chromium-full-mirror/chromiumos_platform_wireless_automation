#!/bin/bash

# To install: 
# apt-get install python-sphinx

sphinx-apidoc  --full --output-dir=output  ../../wireless_automation/
cd output
make html 
gnome-open _build/html/index.html 



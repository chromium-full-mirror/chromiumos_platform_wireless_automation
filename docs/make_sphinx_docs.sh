#!/bin/bash

# To install: 
# apt-get install python-sphinx

export PYTHONPATH=$PYTHONPATH:'../'
sphinx-apidoc  --full --output-dir=sphinx_output  ../wireless_automation/
cd sphinx_output
make html
cp -r _build/html ../output/sphinx


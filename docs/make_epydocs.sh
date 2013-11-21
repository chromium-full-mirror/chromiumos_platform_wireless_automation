#!/bin/bash

#sudo aptitude install python-epydoc

mkdir output
OUTPUT_DIR='output/epydoc'
TO_WIRELESS_AUTOMATION='../'
mkdir $OUTPUT_DIR

PYTHONPATH=$PYTHONPATH:$TO_WIRELESS_AUTOMATION
echo $PYTHONPATH
epydoc --html -o $OUTPUT_DIR --name WirelessAutomation --graph all ../wireless_automation

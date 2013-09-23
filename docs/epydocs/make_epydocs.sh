#!/bin/bash

#sudo aptitude install python-epydoc
PYTHONPATH=$PYTHONPATH:../..
echo $PYTHONPATH
epydoc --html -o html --name WirelessAutomation --graph all ../../wireless_automation
gnome-open html/index.html


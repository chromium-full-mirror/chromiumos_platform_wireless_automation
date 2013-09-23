#!/bin/bash
if [ -z "$1" ]; then 
    echo "No path provided, using ../wireless_automation..."
    location=../wireless_automation/
else
    echo 'passed in path is : '
    echo $1
    location=${1}
fi
echo "about to use ............"
echo $location
pylint --rcfile=pylintrc --report=n --output-format=colorized $location



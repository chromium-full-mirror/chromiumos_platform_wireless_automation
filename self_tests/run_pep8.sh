#!/bin/bash
# E501=max line length. This is checked by pylint, don't do it here
# There are cases where the # pylint disable= directive makes the line
# longer then 80. This is ok, and pylint does not flag it.

# The validate.py and configobj.py files are external projects. They
# are just coppied here. A better way may be to add
# configobj==4.7.
# to the requirements.txt file and remove them from wireless_automation
pep8 --exclude=validate.py,configobj.py --ignore=E501 ../wireless_automation

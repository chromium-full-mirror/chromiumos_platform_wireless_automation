
OUTPUT_DIR='docs/output/uml/'
TO_WIRELESS_AUTOMATION='..'
cd $TO_WIRELESS_AUTOMATION

mkdir $OUTPUT_DIR

pyreverse  \
--output pdf \
--module-names=n \
--ignore=aspects \
-p CoreWirelessAutomation \
wireless_automation/

pyreverse  \
--output pdf \
--module-names=n \
-p EntireWirelessAutomation \
wireless_automation/

mv *.pdf $OUTPUT_DIR
cd $OUTPUT_DIR

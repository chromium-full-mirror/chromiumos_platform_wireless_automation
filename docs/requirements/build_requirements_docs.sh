#!/bin/bash
mkdir output
sphinx-apidoc  --full --output-dir=output ../../radio_tests/
cp index.rst output
cp ../../radio_tests/requirements/*.rst output/
cd output
make html
cd ..
mkdir ../output
cp -r output/_build/html/ ../output/requirements


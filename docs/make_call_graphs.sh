#!/bin/bash
pycallgraph -v graphviz -- ../self_tests/run_all_tests.py
mkdir output
mkdir output/call_graphs
mv pycallgraph.png output/call_graphs

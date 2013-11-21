#!/bin/bash
./make_call_graph_all_test.sh
./make_epydocs.sh
./make_sphinx_docs.sh
./make_uml.sh
cd requirements
./build_requirements_docs.sh


#!/usr/bin/env bash
# Runs unit tests.
# If successful, prints only the coverage percentage.
# If an error occurs, prints the entire unit tests progress output.

source "$(dirname $(realpath $0))/util.sh"

coverage erase
run_and_capture coverage run
coverage report | awk '$1 == "TOTAL" {print $NF; exit}'

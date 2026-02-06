#!/usr/bin/env bash
# Runs unit tests.
# If successful, prints only the coverage percentage.
# If an error occurs, prints the entire unit tests progress output.

source "$(dirname $(realpath $0))/util.sh"

coverage erase
# Capture the test progression in a variable:
typeset progress
progress=$(coverage run 2>&1)
# If tests failed or produced errors, write progress/messages to stderr and exit:
[[ $? -eq 0 ]] || { >&2 echo "${progress}"; exit 1; }
# Otherwise extract the total coverage percentage from the produced report and write it to stdout:
coverage report | awk '$1 == "TOTAL" {print $NF; exit}'

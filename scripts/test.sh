#!/usr/bin/env bash
# Runs unit tests and prints only coverage percentage, if successful.
# If an error occurs, prints the entire unit tests progress output.

# Ensure that we return to the current working directory in case of an error:
trap "cd $(realpath ${PWD})" ERR
# Change into project root directory:
cd "$(dirname $(dirname $(realpath $0)))"

coverage erase
# Capture the test progression in a variable:
typeset progress
progress=$(coverage run 2>&1)
# If tests failed or produced errors, write progress/messages to stderr and exit:
[[ $? -eq 0 ]] || { >&2 echo "${progress}"; exit 1; }
# Otherwise extract the total coverage percentage from the produced report and write it to stdout:
coverage report | awk '$1 == "TOTAL" {print $NF; exit}'

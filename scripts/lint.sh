#!/usr/bin/env bash
# Runs type checker and linters.

# Ensure that we return to the current working directory
# and exit the script immediately in case of an error:
trap "cd $(realpath ${PWD}); exit 1" ERR
# Change into project root directory:
cd "$(dirname $(dirname $(realpath $0)))"

echo 'Performing type checks...'
mypy
echo

echo 'Linting source and test files...'
flake8 src/ tests/
echo -e 'No issues found.'

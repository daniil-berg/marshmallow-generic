#!/usr/bin/env bash
# Runs various linters.

source "$(dirname $(realpath $0))/util.sh"

echo 'Linting source and test files...'

echo '  isort - consistent imports'
isort src/ tests/ --check-only

echo '  ruff - extensive linting'
ruff src/ tests/

echo '  black - consistent style'
run_and_capture black src/ tests/ --check

echo -e "${bold_green}No issues found${color_reset}\n"

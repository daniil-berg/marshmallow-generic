#!/usr/bin/env bash
# Runs various linters.

source "$(dirname $(realpath $0))/util.sh"

echo 'Linting source and test files...'

ruff check src/ tests/
ruff format --check src/ tests/

echo -e "${bold_green}No issues found${color_reset}\n"

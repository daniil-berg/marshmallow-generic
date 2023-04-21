#!/usr/bin/env bash
# Runs unit tests and reports coverage percentage.

source "$(dirname $(realpath $0))/util.sh"

echo 'Running unit tests...'
coverage run
typeset percentage
typeset color
percentage="$(coverage report | awk '$1 == "TOTAL" {print $NF; exit}')"
[[ $percentage == "100%" ]] && color="${bold_green}" || color="${yellow}"
echo -e "${color}${percentage} coverage${color_reset}\n"

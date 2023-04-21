#!/usr/bin/env bash
# Runs type checker.

source "$(dirname $(realpath $0))/util.sh"

echo 'Performing type checks...'
mypy
echo

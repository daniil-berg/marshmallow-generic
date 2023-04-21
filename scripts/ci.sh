#!/usr/bin/env bash
# Runs full CI pipeline (test, typecheck, lint).

typeset scripts_dir="$(dirname $(realpath $0))"

source "${scripts_dir}/util.sh"

"${scripts_dir}/test.sh"
"${scripts_dir}/typecheck.sh"
"${scripts_dir}/lint.sh"

echo -e "${background_black}${bold_green}✅ 🎉 All checks passed!${color_reset}"

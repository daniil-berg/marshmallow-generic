# Ensure that we return to the current working directory
# and exit the script immediately in case of an error:
trap "cd $(realpath ${PWD}); exit 1" ERR
# Change into project root directory:
cd "$(dirname $(dirname $(realpath $0)))"

typeset background_black='\033[40m'
typeset bold_green='\033[1;92m'
typeset yellow='\033[0;33m'
typeset color_reset='\033[0m'

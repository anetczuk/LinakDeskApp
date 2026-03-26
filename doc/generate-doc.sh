#!/bin/bash

set -eu


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


SRC_DIR="$SCRIPT_DIR/../src"


generate_tools_help() {
    HELP_MD_PATH="$SCRIPT_DIR/cmdargs.md"
    HELP_TXT_PATH="$SCRIPT_DIR/cmdargs.txt"

    cd "$SRC_DIR"

    COMMAND="python3 -m linakdeskapp"
    COMMAND_TEXT="linakdeskapp"

    echo "## <a name=\"main_help\"></a> $COMMAND_TEXT --help" > "${HELP_MD_PATH}"
    echo -e "\`\`\`" >> "${HELP_MD_PATH}"
    $COMMAND --help >> "${HELP_MD_PATH}"
    echo -e "\`\`\`" >> "${HELP_MD_PATH}"

    echo -e "\`\`\`" > "${HELP_TXT_PATH}"
    $COMMAND --help >> "${HELP_TXT_PATH}"
    echo -e "\`\`\`" >> "${HELP_TXT_PATH}"


    FAILED=0
    tools=$($COMMAND --listtools 2> /dev/null) || FAILED=1

    if [ $FAILED -eq 0 ]; then
        IFS=', ' read -r -a tools_list <<< "$tools"
    
        for item in "${tools_list[@]}"; do
            echo "checking tool: $item"

            echo -e "\n\n" >> "${HELP_MD_PATH}"
            echo "## <a name=\"${item}_help\"></a> $COMMAND_TEXT $item --help" >> "${HELP_MD_PATH}"
            echo -e "\`\`\`" >> "${HELP_MD_PATH}"
            $COMMAND "$item" --help >> "${HELP_MD_PATH}"
            echo -e "\`\`\`"  >> "${HELP_MD_PATH}"
    
            echo -e "\n\n" >> "${HELP_TXT_PATH}"
            echo -e "\`\`\`" >> "${HELP_TXT_PATH}"
            $COMMAND "$item" --help >> "${HELP_TXT_PATH}"
            echo -e "\`\`\`" >> "${HELP_TXT_PATH}"
        done
    fi
}


generate_tools_help

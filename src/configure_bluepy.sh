#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


configure_caps() {
    local bluepy_path="$1"
    
    local helper_path="$bluepy_path/bluepy-helper"
    if [ ! -f "$helper_path" ]; then
        return 0
    fi

    ## 'cd' is required
    cd $bluepy_path
    echo "Found bluepy site-package path: $bluepy_path"
    
    echo "Current bluepy-helper cap:"
    getcap bluepy-helper
    
    echo "Calling caps on $helper_path"
    sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper
    
    ##sudo setcap cap_net_raw+e "$helper_path"
    ##sudo setcap cap_net_admin+eip "$helper_path"
}


##
## Checking system-wide site-packages
##

paths=$(python3 -c 'import site; [print(item) for item in site.getsitepackages()]' 2> /dev/null)

for site_path in $paths; do
    bluepy_path="$site_path/bluepy"
    configure_caps "$bluepy_path"
done


##
## Checking user local site-packages
##

site_path=$(python3 -m site --user-site 2> /dev/null) || true
bluepy_path="$site_path/bluepy"

configure_caps "$bluepy_path"

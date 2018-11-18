#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"


## add udev rule
AUTOSTART_FILE=~/.config/autostart/LinakDeskControl.desktop


cat > $AUTOSTART_FILE << EOL
[Desktop Entry]
Type=Application
Categories=Office;
Name=LinakDeskControl
GenericName=Linak desk control
Comment=Control Your Linak desk through GUI application
Exec=$SCRIPT_DIR/linakdeskctl --minimized
Icon=$SCRIPT_DIR/linakdeskapp/gui/img/office-chair.png
Terminal=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
EOL


echo "File created in: $AUTOSTART_FILE"

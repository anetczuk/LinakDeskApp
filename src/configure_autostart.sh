#!/bin/bash


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


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
Icon=$SCRIPT_DIR/linakdeskapp/gui/img/office-chair-black.png
Terminal=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
EOL


echo "File created in: $AUTOSTART_FILE"

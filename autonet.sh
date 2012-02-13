#!/bin/bash

# Invoke this script automatically when Wi-Fi location changes.
#
LOCATION_CHANGER=/Library/LaunchAgents/AutoLocationChanger.plist
if [ ! -f $LOCATION_CHANGER ]; then
(
cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key>
 <string>org.metin.vifi</string>
 <key>ProgramArguments</key>
 <array>
  <string>$0</string>
 </array>
 <key>WatchPaths</key>
 <array>
  <string>/Library/Preferences/SystemConfiguration</string>
 </array>
 <key>RunAtLoad</key>
 <true />
</dict>
</plist>
EOF
)  > $LOCATION_CHANGER
launchctl load $LOCATION_CHANGER
fi


if $(networksetup -getairportnetwork en1|grep Verivue > /dev/null); then
    networksetup -setdnsservers Wi-Fi 192.168.3.150
    sudo route add -net 192.168.3 192.168.0.11
    sudo route add -net 192.168.2 192.168.0.11
else
    networksetup -setdnsservers Wi-Fi 8.8.8.8
    sudo route delete -net 192.168.3 192.168.0.11
    sudo route delete -net 192.168.2 192.168.0.11
fi


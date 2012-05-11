#!/bin/bash

OSXVERSION=`sysctl -n kern.osrelease 2> /dev/null`

if [ $? -eq 0 ]; then
    $(mdfind -onlyin /Applications/ Emacs.app)/Contents/MacOS/Emacs $*
else 
    emacs --no-site-file $*
fi


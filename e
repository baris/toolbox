#!/bin/bash

OSXVERSION=`sysctl -n kern.osrelease 2> /dev/null`
if [ $? -eq 0 ]; then
    $(mdfind -onlyin /Applications/ Emacs.app)/Contents/MacOS/Emacs -nw $* 
else 
    emacs -nw $*
fi


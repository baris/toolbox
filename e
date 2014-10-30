#!/bin/bash

OSXVERSION=`sysctl -n kern.osrelease 2> /dev/null`
if [ $? -eq 0 ]; then
    $(mdfind kind:application Emacs.app | head -n 1)/Contents/MacOS/Emacs -nw $*
else
    emacs -nw $*
fi

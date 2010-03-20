#!/bin/bash

OSXVERSION=`sysctl -n kern.osrelease 2> /dev/null`

if [ $? -eq 0 ]; then
    open -a Emacs $*
else 
    emacs --no-site-file $*
fi


#!/bin/bash
#
# also add these to .bashrc
# export EDITOR=e
# export VISUAL=e
#
# also "ln -s `which e` `dirname `which e``/ei"
#

OPTIONS=$*

# Text or Not?
test `basename $0` == "ei"
GRAPHIC_MODE=$?

# Use daemon?
# set E_DAEMON env variable to run emacs daemon.
if [ -n "$E_DAEMON+x" ]
then
    if [ $GRAPHIC_MODE == 0 ]
    then
        OPTIONS="-nw ${OPTIONS}"
    fi
    `which emacs` --no-site-file --geometry 110x55 ${OPTIONS}
else
    # Text or Not?
    if [ $GRAPHIC_MODE == 0 ]
    then
        OPTIONS="-t ${OPTIONS}"
    else
        OPTIONS="-c ${OPTIONS}"
    fi
    `which emacsclient` ${OPTIONS}
    if [ $? != 0 ]
    then
        `which emacs` --no-site-file --daemon
        `which emacsclient` ${OPTIONS}
    fi

fi



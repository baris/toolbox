#!/bin/bash
#
# also add these to .bashrc
# export EDITOR=e
# export VISUAL=e
#
# also "ln -s `which e` `dirname `which e``/ei"
#

EMACSC_OPTIONS=$*
if [ `basename $0` == "ei" ]
then
    EMACSC_OPTIONS="-t ${EMACS_OPTIONS}"
else
    EMACSC_OPTIONS="-c ${EMACS_OPTIONS}"
fi

function emacsd () {
    echo "emacsd!"
    `which emacs` --no-site-file --daemon
}

function emacsc () {
    `which emacsclient` ${EMACSC_OPTIONS}
    if [ $? != 0 ]
    then
        emacsd;
        emacsc;
    fi
}

emacsc

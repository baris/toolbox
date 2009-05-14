#!/bin/bash
#
# also add these to .bashrc
# export EDITOR=e
# export VISUAL=e
#
# also "ln -s `which e` `dirname `which e``/ei"
#

OPTIONS=$*
if [ `basename $0` == "ei" ]
then
    OPTIONS="-t ${OPTIONS}"
else
    OPTIONS="-c ${OPTIONS}"
fi

function emacsd () {
    echo "emacsd!"
    `which emacs` --no-site-file --daemon
}

function emacsc () {
    `which emacsclient` ${OPTIONS}
    if [ $? != 0 ]
    then
        emacsd;
        emacsc;
    fi
}

emacsc

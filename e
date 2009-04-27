#!/bin/bash
#
# also add these to .bashrc
# export EDITOR=e
# export VISUAL=e
# alias ei="e -nw"

exec /usr/bin/emacs --no-site-file $*

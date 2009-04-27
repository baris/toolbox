#!/bin/bash
#
# also add these to .bashrc
# export EDITOR=e
# export VISUAL=e
# alias ei="e -nw -eval (theme-wombat)"

exec /usr/bin/emacs --no-site-file $*

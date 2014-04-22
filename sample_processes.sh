#!/bin/bash

function usage() {
    echo $0 PROCESS_STATE
}

STATE=$1
if [ -z "$STATE" ]; then
    usage
    exit 1
fi

PSOPTS="auxf"
if [ "x$(uname -s)" == "xDarwin" ]; then
    PSOPTS="aux"
fi

while true; do
    date
    $(which ps) "$PSOPTS" | awk -v state=$STATE '{ if($8 == state) print $0; }'
    sleep 1
done

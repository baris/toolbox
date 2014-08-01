#!/bin/bash

# Default interval is 1 second
INTERVAL=${1:-1}

# sums all "total packets received" (ip & ip6)
function get_total_packets ()
{
    netstat -s | awk '/total packets received/ {s += $1} END {print s}'
}

total_packets=$(get_total_packets)
while $(sleep $INTERVAL)
do
    total_packets_new=$(get_total_packets)
    echo $(($total_packets_new - $total_packets))
    total_packets=$total_packets_new
done

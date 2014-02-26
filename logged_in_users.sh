#!/bin/bash

echo $(w -h | awk '{print $1;}' | sort | uniq | tr '\n' ' ')

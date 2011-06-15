#!/bin/bash

if [[ -f TAGS ]]
then
    rm TAGS
fi
find . -name '*.c' -o -name '*.h' -o -name '*.hh' -o -name '*.py' -o -name '*.cc' | xargs -n 1 etags --append

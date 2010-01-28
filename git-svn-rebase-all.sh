#!/bin/bash

for i in `ls`
do 
    if [ -d "${i}/.git/svn" ]
    then
        echo "Working on $i:"
        cd $i
        git svn rebase
        cd -
    fi
done
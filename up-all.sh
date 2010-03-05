#!/bin/bash

BASEDIR=`pwd`

function run_verbose {
    RUNCMD=$1
    RUNDIR=$2
    echo "Running '$RUNCMD' on $RUNDIR"
    cd $RUNDIR;
    eval $RUNCMD;
    cd $BASEDIR;
    echo "done ($RUNDIR)."
    echo -e "\t--------------------"
}

for i in `ls`
do 
    if [ -f "${i}/.git/refs/remotes/git-svn" ]; then
        run_verbose "git svn rebase" ${i}
    elif [ -d "${i}/.git/refs/remotes/origin" ]; then
        run_verbose "git pull origin master" ${i}
    elif [ -d "${i}/.svn/" ]; then
        run_verbose "svn up" ${i}
    fi
done
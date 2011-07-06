#!/bin/bash

function run_verbose {
    RUNCMD=$1
    RUNDIR=$2
    echo "Running '$RUNCMD' on $(pwd)/$RUNDIR"
    pushd $RUNDIR;
    eval $RUNCMD;
    popd
    echo "done ($RUNDIR)."
    echo -e "------\t------\t------\t------\t------\t------\t------"
}

for i in `ls`
do 
    if [ -f "${i}/.git/refs/remotes/git-svn" ]; then
        run_verbose "git svn rebase" ${i}
    elif [ -d "${i}/.git/refs/remotes/origin" ]; then
        run_verbose "git checkout master" ${i}
        run_verbose "git pull" ${i}
    elif [ -d "${i}/.svn/" ]; then
        run_verbose "svn up" ${i}
    fi
done

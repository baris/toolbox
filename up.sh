#!/bin/bash

TMPLOG=$(mktemp /tmp/up.XXXXXXXXXX)

if [[ $1 == "-v" ]]; then
    VERBOSE=1
    shift
fi

function _msg {
    if [[ $VERBOSE -eq 1 ]]; then
        echo -e $1
    fi
}

function _run {
    if [[ $2 -eq 1 ]]; then
        $(eval $1)
    else
        :> $TMPLOG
        eval $1 > $TMPLOG 2>&1
        if [ $? -ne 0 ]; then
            echo $(cat $TMPLOG)
        fi
    fi
}

function run {
    RUNCMD=$1
    RUNDIR=$2
    _msg "Running '$RUNCMD' on $(pwd)/$RUNDIR"
    _run 'pushd $RUNDIR'
    _run 'eval $RUNCMD'
    _run 'popd'
}

function git_branch () {
    pushd $1 > /dev/null
    gitbranch=$(git symbolic-ref HEAD 2> /dev/null)
    gitbranch=${gitbranch#refs/heads/}
    popd > /dev/null
    echo $gitbranch
}

for i in `ls`
do 
    echo "#### Working on ${i} ####"
    if [ -f "${i}/.git/refs/remotes/git-svn" ]; then
        run "git svn rebase" ${i}
    elif [ -d "${i}/.git/refs/remotes/origin" ]; then
        CUR_BRANCH=$(git_branch ${i})
        if [[ x$CUR_BRANCH != "xmaster" ]]; then
            _msg "Changing current branch from ${CUR_BRANCH} to master"
            run "git checkout master" ${i}
        fi
        run "git pull" ${i}
        if [[ x$CUR_BRANCH != "xmaster" ]]; then
            run "git checkout $CUR_BRANCH" ${i}
            run "git pull" ${i}
        fi
    elif [ -d "${i}/.hg/" ]; then
        run "hg pull" ${i}
        run "hg up" ${i}
    elif [ -d "${i}/.svn/" ]; then
        run "svn up" ${i}
    fi
done

rm -f $TMPLOG

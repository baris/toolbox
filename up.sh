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

function update_directory() {
    DIR=$1
    IS_REPOSITORY=1
    echo "#### Working on ${PWD}/${DIR} ####"
    if [ -f "${DIR}/.git/refs/remotes/git-svn" ]; then
        run "git svn rebase" ${DIR}
    elif [ -d "${DIR}/.git/refs/remotes/origin" ]; then
        CUR_BRANCH=$(git_branch ${DIR})
        if [[ x$CUR_BRANCH != "xmaster" ]]; then
            _msg "Changing current branch from ${CUR_BRANCH} to master"
            run "git checkout master" ${DIR}
        fi
        run "git pull" ${DIR}
        if [[ x$CUR_BRANCH != "xmaster" ]]; then
            run "git checkout $CUR_BRANCH" ${DIR}
            run "git pull" ${DIR}
        fi
    elif [ -d "${DIR}/.hg/" ]; then
        run "hg pull" ${DIR}
        run "hg up" ${DIR}
    elif [ -d "${DIR}/.svn/" ]; then
        run "svn up" ${DIR}
    else
        IS_REPOSITORY=0
    fi
    return $IS_REPOSITORY
}

function update_directory_rec() {
    if [ $# -eq 0 ]; then
        return
    fi
    update_directory $1
    if [ $? -ne 1 ]; then
        pushd $1 > /dev/null
        update_directory_rec $(ls)
        popd > /dev/null
    else
        shift 1
        update_directory_rec $@
    fi
}

update_directory_rec $(ls)

rm -f $TMPLOG

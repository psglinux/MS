#!/bin/bash
#########################################
# author : Team Elfs
# script : bash script for build and install of cmpe-272
#########################################

#!/bin/bash

ADIR=assignments

function travis_build() {
    echo "Building using Travis..."
    pushd $ADIR
    echo $PWD
    ./deploy.sh -b
    popd
}

function travis_test_deploy() {
    echo "Deploy Testing Using Travis..."
    pushd $ADIR
    echo $PWD
    ./deploy.sh -i
    sleep 3
    ./deploy.sh -s
    sleep 3
    ./deploy.sh -c
    popd

}

function travis_unit_test() {
    echo "Unit Testing Book API !!"
    pushd $ADIR
    python3.6 bookapi_ut.py
    python3.6 addcustapi_ut.py
    python3.6 addorderapi_ut.py
    python3.6 bookstore_flask_ut.py -v
    popd
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-d] [-t] [-h]
This script is for build, deply and test using Travis

    -b          build the assignment
    -d          test deploy assignemnt
    -t          unit test assignments
    -h          help
EOF
    exit 1;
}

function main() {

    if [[ $# -eq 0 ]] ; then
        usage
        exit 0
    fi

    while getopts "bdth" o; do
        case "${o}" in
        b)
            travis_build
            ;;
        d)
            travis_test_deploy
            ;;
        t)
            travis_unit_test
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
        esac
    done
    shift 0

}

main $@


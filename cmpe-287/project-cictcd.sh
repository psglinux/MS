#!/bin/bash
###################################################################
# author :
# script : bash script for build and install of cmpe-287 project
###################################################################

#!/bin/bash

PDIR=iot5g
BUILDFILE=iot5g-project.sh

function travis_build_project() {
    echo "Building using Travis..."
    pushd $PDIR
    echo $PWD
    ./BUILDFILE -b
    popd
}

function travis_test_deploy_project() {
    echo "deploy-project Testing Using Travis..."
    pushd $PDIR
    echo $PWD
    ./BUILDFILE -i
    sleep 3
    ./BUILDFILE -s
    sleep 3
    ./BUILDFILE -c
    popd

}

function travis_unit_test_project() {
    echo "Unit Testing Book API !!"
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-d] [-t] [-h]
This script is for build, deply and test of Team Elfs project using Travis

    -b          build the project
    -d          test deploy assignment
    -t          unit test project
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
            travis_build_project
            ;;
        d)
            travis_test_deploy_project
            ;;
        t)
            travis_unit_test_project
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


#!/bin/bash
###################################################################
# author : Team Elfs
# script : bash script for build and install of cmpe-272 project
###################################################################

#!/bin/bash

PDIR=project

function travis_build_project() {
    echo "Building using Travis..."
    pushd $PDIR
    echo $PWD
    ./deploy-project.sh -b
    popd
}

function travis_test_deploy_project() {
    echo "deploy-project Testing Using Travis..."
    pushd $PDIR
    echo $PWD
    ./deploy-project.sh -i
    sleep 3
    ./deploy-project.sh -s
    sleep 3
    ./deploy-project.sh -c
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


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

function travis_deploy() {
    echo "Deplying using Travis..."
}

function travis_unit_test() {
    echo "Unit Testing Using Travis..."
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-d] [-t] [-h]
This script is for build, deply and test using Travis 

    -b          build the assignment 
    -d          deploy assignemnt 
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

    while getopts "bcth" o; do
        case "${o}" in
        b)
            travis_build
            ;;
        c)
            travis_deploy
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


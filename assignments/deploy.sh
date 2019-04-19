#!/bin/bash
#########################################
# author : Team Elfs
# script : bash script for build and install of cmpe-272
#########################################

#!/bin/bash

DCRFLASK=elfs-flask
DCRNGNX=elfs-nginx
DCRNET=elfs-network
DCRMONGODB=elfs-mongodb
DCRNGNXNAME=nginx
DCRFLASKNAME=flask
DCRMONGODBNAME=mongodb

function build_elfs_app() {
    echo "Building ...."
	docker build -t $DCRFLASK -f Dockerfile-flask .
	docker build -t $DCRNGNX -f Dockerfile-nginx .
	docker build -t $DCRMONGODB -f Dockerfile-mongodb .
}

function deploy_elfs_app() {
    echo "Deploying Team Elf's webserver and application..."

	docker network create $DCRNET
	docker run -d --name $DCRFLASKNAME --net $DCRNET -v "./app" $DCRFLASK
	docker run -d --name $DCRNGNXNAME --net $DCRNET -p "80:80" $DCRNGNX
	docker run -d --name $DCRMONGODBNAME -d -v /tmp/mongodb:/data/db -p 27017:27017 $DCRMONGODB

}

function clean_elfs_app() {
    echo "Cleaning Team Elfs webserve and applicatio..."
    docker kill $DCRFLASKNAME $DCRNGNXNAME
    docker rm $DCRFLASKNAME $DCRNGNXNAME
    docker network rm $DCRNET
    docker rmi $DCRNGNX $DCRFLASK
    docker rm $DCRMONGODBNAME $DCRMONGODBNAME
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-c] [-i] [-h]
This script is for build and deploy webserver and application

    -b          build the containers needed for deployment
    -c          clean the containers
    -i          start the containers  webserver, uwsgi, app server and mongodb
    -h          help
EOF
    exit 1;
}

function main() {
    
    if [[ $# -eq 0 ]] ; then
        usage
        exit 0
    fi
    
    while getopts "bcih" o; do
        case "${o}" in
        b)
            build_elfs_app
            ;;
        c)
            clean_elfs_app
            ;;
        i)
            deploy_elfs_app
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


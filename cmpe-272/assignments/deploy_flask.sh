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
MONGODBPERSIST=/var/www/mongodb

function create_mongo_db_dir() {
    if [ ! -d $MONGODBPERSIST ]; then
        echo "creating persistent mongodb directory"
        mkdir -p $MONGODBPERSIST
    fi
}

function build_elfs_app() {
    echo "Building ...."
	docker build -t $DCRFLASK -f Dockerfile-flask .
}

function deploy_elfs_app() {
    echo "Deploying Team Elf's webserver and application..."

    #create_mongo_db_dir
	docker run -d --name $DCRFLASKNAME --net $DCRNET -v "./app" $DCRFLASK
    docker ps

}

function clean_elfs_app() {
    echo "Cleaning Team Elfs webserve and applicatio..."
    docker kill $DCRFLASKNAME
    docker rm $DCRFLASKNAME 
    docker rmi $DCRFLASK
}

function stop_elfs_app() {
    echo "Stopping Team Elfs webserve and applicatio..."
    docker kill $DCRFLASKNAME
    docker rm $DCRFLASKNAME 
    docker ps
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-c] [-i] [-h]
This script is for build and deploy webserver and application

    -b          build the containers needed for deployment
    -c          clean the containers, (stop and clean the container images)
    -i          start the containers  webserver, uwsgi, app server and mongodb
    -s          stop the running containers
    -h          help
EOF
    exit 1;
}

function main() {

    if [[ $# -eq 0 ]] ; then
        usage
        exit 0
    fi

    while getopts "bcihs" o; do
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
        s)
            stop_elfs_app
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

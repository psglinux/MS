#!/bin/bash
#########################################
# author : Team Elfs
# script : bash script for building the iot docker infra
#          original source code from bash cmpe-272
#########################################

IOTDOCKER=elfs-project-iot5g
IOTDOCKERNAME=project-iot5g
NFV5GDOCKER=elfs-project-nfv5g
NFV5GDOCKERNAME=project-nfv5g
IOTCLOUDDOCKER=elfs-project-iotcloud
IOTCLOUDDOCKERNAME=project-iotcloud

DCRNET=elfs-project-network
#DCRMEMCHD=elfs-project-memcached
#DCRMEMCHDNAME=project-memcached

# Copy over CSV files to the following location
CSVIMPORTPATH=testdb
MONGOPORT=27017
MEMCHDPORT=11211

function copy_files_from_assignment()
{
    mkdir common
    cp ../assignments/login.py common/
    cp ../assignments/apymongodb.py common/
    cp ../assignments/app.py common/
    cp ../assignments/bookapi.py common/
    cp ../assignments/addorderapi.py common/
}
function clean_assignment_files()
{
    rm -rf common
}

function create_mongo_db_dir() {
    if [ ! -d $MONGODBPERSIST ]; then
        echo "creating persistent mongodb directory"
        mkdir -p $MONGODBPERSIST
    fi
}

function build_elfs_project_app() {
    echo "Building ...."

    docker build -t $IOTDOCKER -f Dockerfile-iot5g .
    docker build -t $NFV5GDOCKER -f Dockerfile-nfv5g .
    docker build -t $IOTCLOUDDOCKER -f Dockerfile-iotcloud .
    #docker build -t $DCRMEMCHD -f Dockerfile-project-memcached .
    #copy_files_from_assignment
    clean_assignment_files
}

function deploy_elfs_project_app() {
    echo "Deploying Team Elf's webserver and application..."

    #create_mongo_db_dir
    docker network create $DCRNET
    docker run -d --name $IOTDOCKERNAME --net $DCRNET  $IOTDOCKER
    docker run -d --name $NFV5GDOCKERNAME --net $DCRNET  $NFV5GDOCKER
    docker run -d --name $IOTCLOUDDOCKERNAME --net $DCRNET  $IOTCLOUDDOCKER
    #docker run -d --name $DCRMEMCHDNAME --net $DCRNET -p $MEMCHDPORT:$MEMCHDPORT -e MEMCACHED_MEMUSAGE=32 $DCRMEMCHD
    docker ps
}

#function import_csv_data() {
#    #import the user db
#    python3 apymongodb.py localhost
#    echo "Importing CSV data from $CSVIMPORTPATH ..."
#    if [ ! -d $CSVIMPORTPATH ]; then
#        echo "No such directory"
#        exit 1
#    fi
#    for entry in $CSVIMPORTPATH/*.csv; do
#        echo "Importing $entry into DB"
#        collname=$(basename  $entry .csv)
#        python3 tools/batch_import.py localhost:$MONGOPORT $entry $collname
#    done
#}

function clean_elfs_project_app() {
    echo "Cleaning Team Elfs webserve and applicatio..."

    #docker kill $IOTDOCKERNAME $DCRMEMCHDNAME $NFV5GDOCKERNAME $IOTCLOUDDOCKERNAME
    docker kill $IOTDOCKERNAME $NFV5GDOCKERNAME $IOTCLOUDDOCKERNAME
    docker network rm $DCRNET
    #docker rmi $IOTDOCKER $DCRMEMCHD $NFV5GDOCKER $IOTCLOUDDOCKER
    docker rmi $IOTDOCKER $NFV5GDOCKER $IOTCLOUDDOCKER
}

function stop_elfs_project_app() {
    echo "Stopping Team Elfs webserve and applicatio..."

    #docker kill $IOTDOCKERNAME $DCRMEMCHDNAME $NFV5GDOCKERNAME $IOTCLOUDDOCKERNAME
    #docker rm $IOTDOCKERNAME $DCRMEMCHDNAME $NFV5GDOCKERNAME $IOTCLOUDDOCKERNAME
    docker kill $IOTDOCKERNAME $NFV5GDOCKERNAME $IOTCLOUDDOCKERNAME
    docker rm $IOTDOCKERNAME $NFV5GDOCKERNAME $IOTCLOUDDOCKERNAME
    docker network rm $DCRNET
    docker ps
}

# Usage info
usage() {
#    -p          import CSV data into mongodb
cat << EOF
Usage: ${0##*/} [-b] [-p] [-c] [-i] [-h]
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

    while getopts "bpcihs" o; do
        case "${o}" in
        b)
            build_elfs_project_app
            ;;
#        p)
#            import_csv_data
#            ;;
        c)
            clean_elfs_project_app
            ;;
        i)
            deploy_elfs_project_app
            ;;
        s)
            stop_elfs_project_app
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


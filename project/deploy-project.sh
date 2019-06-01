#!/bin/bash
#########################################
# author : Team Elfs
# script : bash script for build and install of cmpe-272
#########################################

DCRFLASK=elfs-project-flask
DCRLOGINFLASK=elfs-project-login-flask
DCRNGNX=elfs-project-nginx
DCRNET=elfs-project-network
DCRMONGODB=elfs-project-mongodb
DCRMEMCHD=elfs-project-memcached
DCRNGNXNAME=nginx
DCRFLASKLOGINNAME=project-login-flask
DCRFLASKNAME=project-flask
DCRMONGODBNAME=project-mongodb
MONGODBPERSIST=/var/www/project-mongodb
DCRMEMCHDNAME=project-memcached

# Copy over CSV files to the following location
CSVIMPORTPATH=/var/data/csv
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
    docker build -t $DCRFLASK -f Dockerfile-project-flask .
    docker build -t $DCRNGNX -f Dockerfile-project-nginx .
    docker build -t $DCRMONGODB -f Dockerfile-project-mongodb .
    docker build -t $DCRMEMCHD -f Dockerfile-project-memcached .
    #copy_files_from_assignment
    docker build -t $DCRLOGINFLASK -f Dockerfile-project-login-flask .
    clean_assignment_files
}

function deploy_elfs_project_app() {
    echo "Deploying Team Elf's webserver and application..."

    #create_mongo_db_dir
    docker network create $DCRNET
    docker run -d --name $DCRFLASKNAME --net $DCRNET -v "./projectapp" $DCRFLASK
    docker run -d --name $DCRNGNXNAME --net $DCRNET -p "80:80" $DCRNGNX
    docker run -d --name $DCRMONGODBNAME --net $DCRNET -d -v $MONGODBPERSIST:/data/db -p $MONGOPORT:$MONGOPORT $DCRMONGODB
    docker run -d --name $DCRMEMCHDNAME --net $DCRNET -p $MEMCHDPORT:$MEMCHDPORT -e MEMCACHED_MEMUSAGE=32 $DCRMEMCHD
    docker run -d --name $DCRFLASKLOGINNAME --net $DCRNET -v "./login" $DCRLOGINFLASK
    docker ps
}

function import_csv_data() {
    echo "Importing CSV data from $CSVIMPORTPATH ..."
    if [ ! -d $CSVIMPORTPATH ]; then
        echo "No such directory"
        exit 1
    fi
    for entry in $CSVIMPORTPATH/*.csv; do
        echo "Importing $entry into DB"
        collname=$(basename  $entry .csv)
        python3 tools/batch_import.py localhost:$MONGOPORT $entry $collname
    done
}

function clean_elfs_project_app() {
    echo "Cleaning Team Elfs webserve and applicatio..."
    docker kill $DCRFLASKNAME $DCRNGNXNAME $DCRFLASKLOGINNAME $DCRMONGODBNAME $DCRMEMCHDNAME
    docker rm $DCRFLASKNAME $DCRNGNXNAME $DCRFLASKLOGINNAME $DCRMONGODBNAME $DCRMEMCHDNAME
    docker network rm $DCRNET
    docker rmi $DCRNGNX $DCRFLASK $DCRMONGODB $DCRMEMCHD
}

function stop_elfs_project_app() {
    echo "Stopping Team Elfs webserve and applicatio..."
    docker kill $DCRFLASKNAME $DCRNGNXNAME $DCRFLASKLOGINNAME $DCRMONGODBNAME $DCRMEMCHDNAME
    docker rm $DCRFLASKNAME $DCRNGNXNAME $DCRFLASKLOGINNAME $DCRMONGODBNAME $DCRMEMCHDNAME
    docker network rm $DCRNET
    docker ps
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-p] [-c] [-i] [-h]
This script is for build and deploy webserver and application

    -b          build the containers needed for deployment
    -p          import CSV data into mongodb
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
        p)
            import_csv_data
            ;;
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


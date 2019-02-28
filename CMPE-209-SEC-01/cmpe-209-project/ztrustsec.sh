#!/bin/bash
###################################################
# author : psglinux@gmail.com
# script : bash script to create 
#          i. docker container 
#         ii. network elements for the zero trust container
#        iii. configure suricata in the container
###################################################

#!/usr/bin/env bash

#packets on this iface in the vm would be punted to the docker
HVM_IF=${HVM_IF:-ens38}
D_SRC_DIR=${D_SRC_DIR:-/home/psg/working/MS/CMPE-209-SEC-01/project}
D_INST_DIR=${D_INST_DIR:-/tmp/docker-suricata}
D_MACVLAN_NET=mvlan4-net
HOST_DOCKER_VBRDG_NAME=privnet
D_CONT_NAME=${D_CONT_NAME:-mycontainer}
ZS_TAG=ztrustsec
ZS_CONT_IMG_ID=
D_IFACE_CFG=docker_iface_configure.sh

set +e

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-b] [-c] [-C] [-d] [-h] [-I] [-n] [r] [R]
This script is for installation of the needed debian packages

    -b          build a docker image 
    -c          test the docker installation
    -d          delete the docker container
    -n          create the network 
    -r          delete the docker network configuration
    -C          test the docker installation and the network connectivity  
    -I          create a docker image and the network
    -R          delete the docker installation and the netwroking configuration 
    -h          help
EOF
    exit 1;
}


check_docker_installation () {
    echo ${FUNCNAME[0]}
    echo "... checking if the docker image exists"
    arr=($(sudo docker image ls | grep $ZS_TAG))
    echo ${arr[@]}
    if [ 0 -ne ${#arr[@]} ] ; then
        echo "...... docker file image exists"
        ZS_CONT_IMG_ID=${arr[2]}
        echo "...... docker id is "$ZS_CONT_IMG_ID
        return 1
    else
      echo "...... docker image does not exists for this, create a docker image "
    fi
    return 0
}

check_docker_network () {
    echo ${FUNCNAME[0]}
}    

create_docker_install_dir() {
    if [ ! -f $D_SRC_DIR/Dockerfile ]; then
        echo "... "$var"-docker.sh installation script not found locally"
        #TBD : download from the Dockerfile from a remote location
    fi
    if [ ! -d $D_INST_DIR ]; then 
            mkdir -p $D_INST_DIR/log
    fi
    echo "... copied docker file from "$D_SRC_DIR" to "$D_INST_DIR
    cp $D_SRC_DIR/Dockerfile $D_INST_DIR 
    echo "... copied initial network configuration file from "$D_SRC_DIR" to "$D_INST_DIR
    cp -f $D_SRC_DIR/docker_iface_configure.sh $D_INST_DIR/start.sh
    chmod a+x $D_INST_DIR/start.sh
}

find_zsec_container_id() {
    echo ${FUNCNAME[0]}
    echo "... checking if the docker image exists"
    arr=($(sudo docker image ls | grep $ZS_TAG))
    echo ${arr[@]}
    if [ 0 -ne ${#arr[@]} ] ; then
        echo "...... docker file image exists"
        ZS_CONT_IMG_ID=${arr[2]}
    else
      echo "...... docker image does not exists for this, create a docker image "
      exit 1
    fi
}

build_suricate_docker() {
    cd $D_INST_DIR
    echo "... building docker for suricata"
    check_docker_installation
    if [ 0 -eq $? ]; then
        echo "...... building docker image for the ztrustsec"
        echo "...... it could take about 10 mintes for this, as the image is needs to be built"
	sudo apt-get update
        time sudo docker build -t $ZS_TAG ./| tee $D_INST_DIR/log/install.log
    fi
    cd -
}

install_suricata_docker () {
    echo ${FUNCNAME[0]}
    create_docker_install_dir
    build_suricate_docker
}    

zsec_start_docker() {
    echo "... starting the docker container"
    sudo docker start $D_CONT_NAME
    echo "... Attaching to the container"
    sudo docker exec -it $D_CONT_NAME bash ###TBD add the script here to configure the docker
    #sudo docker exec -it $D_CONT_NAME sh -c ./$D_IFACE_CFG

}

create_network_elem_vm() {
    echo ${FUNCNAME[0]}
    echo "... creating the network element in vm for ztrustsec"
    echo "... creating macvlan network on the docker"
    sudo docker network create -d macvlan -o parent=$HVM_IF -o macvlan_mode=passthru $D_MACVLAN_NET 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "...... created macvlan network on the docker"
    else
        echo "...... macvlan network on the docker already exists"
    fi
    echo "... creating the private network"
    sudo docker network create $HOST_DOCKER_VBRDG_NAME 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "...... created private network for the communication between vm and docker" 
    else
        echo "...... private network exists for the communication between vm and docker" 
    fi
    echo "... creating the docker container "
    sudo docker create -it --privileged --net $D_MACVLAN_NET --name $D_CONT_NAME $ZS_CONT_IMG_ID 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "...... docker container "$ZS_CONT_IMG_ID "successfully created" 
    else
        echo "...... docker container "$ZS_CONT_IMG_ID "already exists" 
    fi
    echo "... connecting the docker network with the virtual bridge on the vm"
    sudo docker network connect $HOST_DOCKER_VBRDG_NAME $D_CONT_NAME 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "... successfully connected the docker network " $D_CONT_NAME" with the virtual bridge "$HOST_DOCKER_VBRDG_NAME" on the vm"
    else
        echo "... connection of the docker network " $D_CONT_NAME" with the virtual bridge "$HOST_DOCKER_VBRDG_NAME" on the vm exits"
    fi
}

install_docker_network () {
    echo ${FUNCNAME[0]}
    find_zsec_container_id
    create_network_elem_vm    
    zsec_start_docker
}

delete_docker_install_dir() {
    echo ${FUNCNAME[0]}
    echo "... removing the tmp dirrectory for install "$D_INST_DIR
    if [ -d $D_INST_DIR ]; then 
            rm -rf $D_INST_DIR
    fi
}

delete_docker_img() {
    check_docker_installation
    if [ 0 -eq $? ]; then
        echo "...... docker installation does not exists"
        return 1
    fi
    echo "... removing docker image "$ZS_CONT_IMG_ID" forcefully"
    sudo docker rmi $ZS_CONT_IMG_ID --force
    sudo docker image ls
}

uninstall_suricata_docker () {
    echo ${FUNCNAME[0]}
    delete_docker_img
    delete_docker_install_dir
}

delete_network_elem_vm() {
    echo ${FUNCNAME[0]}
    echo "... deleting the network element in vm for ztrustsec"
    echo "... stopping the docker container"
    sudo docker stop $D_CONT_NAME
    if [ 0 -eq $? ]; then
        echo "...... docker container "$ZS_CONT_IMG_ID "successfully stopped" 
    else
        echo "...... docker container "$ZS_CONT_IMG_ID "already stopped" 
    fi
    echo "... deleting the docker container "
    sudo docker rm -it --privileged --net $D_MACVLAN_NET --name $D_CONT_NAME $ZS_CONT_IMG_ID 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "...... docker container "$ZS_CONT_IMG_ID "successfully removed" 
    else
        echo "...... docker container "$ZS_CONT_IMG_ID "already removed" 
    fi
    echo "... deleting macvlan network on the docker"
    sudo docker network rm $D_MACVLAN_NET 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "...... deleted macvlan network on the docker"
    else
        echo "...... macvlan network on the docker already deleted"
    fi
    echo "... deleting the private network"
    sudo docker network rm $HOST_DOCKER_VBRDG_NAME 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "...... created private network for the communication between vm and docker" 
    else
        echo "...... private network exists for the communication between vm and docker" 
    fi
    echo "... disconnecting the docker network with the virtual bridge on the vm"
    sudo docker network connect $HOST_DOCKER_VBRDG_NAME $D_CONT_NAME 2> $D_INST_DIR/log/error.log
    if [ 0 -eq $? ]; then
        echo "... successfully disconnected the docker network " $D_CONT_NAME" with the virtual bridge "$HOST_DOCKER_VBRDG_NAME" on the vm"
    else
        echo "... docker network " $D_CONT_NAME" with the virtual bridge "$HOST_DOCKER_VBRDG_NAME" on the vm is disconnected"
    fi
}

uninstall_docker_network () {
    echo ${FUNCNAME[0]}
    delete_network_elem_vm
}

validate_args() {
    #check if more then 1 args
    if [ $# -lt 1 ]; then
        echo 1>&2 "$0: not enough arguments"
        usage
    fi
}

print_assumptions() {
cat << EOF
    This installer script assumes the following items
        i. the vm on which this scirpt is running has 3 interface,
EOF
}

#scripts starts here 

echo $#
#validate_args

while getopts ":bcdnrhICR" o; do
    case "${o}" in
        b)
            #i=${OPTARG}
            install_suricata_docker 
            exit 0
            ;;
        c)
            #i=${OPTARG}
            check_docker_installation
            check_docker_network 
            exit 0
            ;;
        d)
            #d=${OPTARG}
            uninstall_suricata_docker
            exit 0
            ;;
        n)
            #n=${OPTARG}
            install_docker_network
            exit 0 
            ;;
        r)
            #r=${OPTARG}
            uninstall_docker_network
            exit 0 
            ;;
        C)
            #C=${OPTARG}
            check_docker_installation
            check_docker_network
            ;;
        I)
            install_suricata_docker
            install_suricata_docker
            #I=${OPTARG}
            ;;
        R)
            #R=${OPTARG}
            uninstall_docker_network
            uninstall_suricata_docker
            ;;
        h|*)
            usage
            ;;
    esac
done
shift $((OPTIND-1))


#echo "... s = ${s}"
#echo "... p = ${p}"
#echo "... c = ${c}"

set -e

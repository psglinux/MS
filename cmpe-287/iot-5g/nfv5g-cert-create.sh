#!/bin/bash
#########################################
# author : Partha S. Ghosh
# script : bash script for building the iot docker infra
#          original source code from bash cmpe-272
#########################################

TMP_CERT_DIR="nfv-cert"
CA_KEY=$TMP_CERT_DIR/ca.key
CA_CRT=$TMP_CERT_DIR/ca.crt
SERV_KEY=$TMP_CERT_DIR/server.key
SERV_CSR=$TMP_CERT_DIR/server.csr
SERV_CRT=$TMP_CERT_DIR/server.crt
CERT_DURATION=10

function create_self_signed_certificate() {
    #First create a key pair for the CA, you can password protect the CA
    openssl genrsa -des3 -out $CA_KEY 2048
    #Now Create a certificate for the CA using the CA key
    openssl req -new -x509 -days 1826 -key $CA_KEY -out $CA_CRT
    #Now we create a server key pair that will be used by the broker
    openssl genrsa -out $SERV_KEY 2048

    # Now we create a certificate request .csr. When filling out the form the
    # common name is important and is usually the domain name of the server.
    # Because the demonstration is a container enviornment, we need to use the
    # domain name of the container enviornemnet. The Mosquitto broker which is
    # using elfs-project-networks. One could use the IP address or FQDN.
    # NOTE : this is the domain that needs to be used while configuring the
    # MQTTclient connection.

    openssl req -new -out $SERV_CSR -key $SERV_KEY

    # Now we use the CA key to verify and sign the server certificate. This creates the $SERV_CRT file
    openssl x509 -req -in $SERV_CSR -CA $CA_CRT -CAkey $CA_KEY -CAcreateserial -out $SERV_CRT -days 10

}

function create_cert_dir()
{
    if [ ! -d $TMP_CERT_DIR ]; then
        mkdir $TMP_CERT_DIR
    fi
}

# Usage info
usage() {
cat << EOF
Usage: ${0##*/} [-c] [-h]
This script is to create certificates for nfv5g servers

    -c          create certificates
    -h          help
EOF
    exit 1;
}

function main() {

    if [[ $# -eq 0 ]] ; then
        usage
        exit 0
    fi

    while getopts "ch" o; do
        case "${o}" in
        c)
            create_cert_dir
            create_self_signed_certificate
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


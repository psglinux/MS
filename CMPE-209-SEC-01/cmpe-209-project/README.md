#cmpe-209-project


TL;DR

# Zero Trust Security Approach to Server Application
## A containerized approach for IPS

###Abstract
#### The evolution of cloud infrastructure has necessitated changes in traditional IDS/IPS for applications as well as policy management. This project aims to prototype a container based IDS/IPS for application deployed in VMs. The project intends to develop a working container which would perform IDS/IPS for any traffic to and from a VM. The project also intends to demonstrate a few test cases as how this security contianer would be used. The project intends to use

 1. docker containers
 2. suricata (https://suricata-ids.org/) as the IDS/IPS
 3. Linux namespace to keep the security module and applications in separate network domain.


## How to Run
```
HVM_IF=ens4 D_SRC_DIR=$PWD D_CONT_NAME=<container-name> ./ztrustsec.sh -I
HVM_IF=ens4 D_SRC_DIR=$PWD D_CONT_NAME=<container-name> ./ztrustsec.sh -n
```

## Source Code
*  ztrustsec.sh (The master script)
*   docker_iface_configure.sh
*   Dockerfile (ubuntu suricata docker File)
*   http-server.py (demo simple and stupid http server in python using bottle)
*   namespace.sh (an expriment script for network isolation using Namespace)






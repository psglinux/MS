## Summary of steps that done in the deployment scripts (step 2-$s)
1. Create a Ubuntu VM with > 3 interfaces. One for SSH and 2 extra to pass into docker container
2. Install Docker on it
3. Create a work-dir on the VM (mkdir -p workdir; cp Dockerfile workdir/)
4. Create a macvlan docker network -> 
"sudo docker network  create -d macvlan -o parent=ens4 -o macvlan_mode=passthru ens4mvlan". 
In this case we are using ens4 as the NIC inside the VM over which we will put macvlan. Do not use the same nic as the one being used for ssh.
5. cd workdir
6. sudo docker build ./
7. Look at the image ID dumped by command in #6 -- say "2ae5c37d52f9"
8. sudo docker network create privnet8 
9. sudo docker create -it --privileged --net ens4mvlan --name privnet --name mycontainer 2ae5c37d52f9
10. sudo docker network connect privnet mycontainer
11. sudo docker start mycontainer
12. sudo docker exec -it mycontainer bash
13. sudo docker stop mycontainer
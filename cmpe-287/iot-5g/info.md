# Information about tools, methodology and how to use the code in this project
This information file document on some of the common tools and techniques that is being used to analyze the latency study that is being performed for IOT devices with respect to cloud and edge computing.


## Debug Artifacts
A number of debug output has been created which are used a mesaurement artifacts. These includes packet capture in different circumstances, output to understand behavior of a secure server using tls etc

The location of these artifacts are in *iot-5g/debug* directory

## Mosquitto
Mosquitto broker is being used here to simulate the IOT broker (this would be a 5G gateway NFV). The Mosquitto broker would be configrued to use TLS. In essence of the nature of the project (prototype) a self signed certificate would be used. The domain of the PKI for the IOT devices is beyond the scope of this project. 
The Goal is to establish a encrypted connection between the MQTT broker (nfv5g) and the MQTT client (iot5g). MQTT broker certificate would be the only Trusted (self signed) certificate created. Client certificates would not be needed for this demonstration. In essecne for the secure communication
1. the client would need a CA (certificate authority) certificate of the CA that has signed the server certificate on the Mosquitto Server.
2. The MQTT broker would 
    - CA certificateof the CA (Certificate Authority) that has signed the Server certificate on the Mosquitto Broker.
    - CA certified server certificate
    - Server Private key for decryption

### Creating the Self signed Server Certificate 


### verifying certificate

`psg@psglinux:~/working/MS/CMPE-287/cmpe-287/iot-5g/nfv-cert$openssl verify -CAfile ca.crt server.crt
server.crt: C = US, ST = CA, L = San Jose, O = Elfs, OU = iot5g, CN = elfs-project-networks, emailAddress = parthasarathi.ghosh@sjsu.edu
error 18 at 0 depth lookup:self signed certificate
OK`

### Starting the mosquitto server
connect to docker
`
/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf -v
`

### Starting the mosquitto client

`mosquitto_pub -h <mqtt-server-ip-address> -m "test message" -t house/bulb1 --cafile /etc/mosquitto/ca_certificates/ca.crt -p 8883 --insecure
`
## Useful Tools and Utilities in Analysing Performance

## dumping tcpdump stat from the host to the containers

`docker exec -it project-nfv5g tcpdump -i eth0 port 8883`
`docker exec -it project-nfv5g tcpdump -i eth0 port 8883`
`docker exec -it project-nfv5g tcpdump -i eth0 port 8883`

### use xpane (tmux extension) for monitoring the traffic
`docker ps -q | xpanes -s -c "docker exec -it {} tcpdump -i eth0 port 8883"`

### Capture the tcpdump for packet analysis for secure mq
tt packets
tcpdump is the go to tool that any programmer would use to analyze network traffic. With the right set of filters in the command line the requisite network data could be filtered with ease. Note that the pcap file could then be used with utility libs for pcap to perform analysis.

*tcpdump port 8883 -i ens33  -w <pcapfile-name>*

### command to verify if the remote server supports ssl key renegotiation
*openssl s_client -connect iot.eclipse.org:8883*

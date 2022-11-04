[![Build Status](https://travis-ci.com/psglinux/cmpe-287.svg?branch=master)](https://travis-ci.com/psglinux/cmpe-287)

# Project for SJSU CMPE-287

    - This base code for this project is from [[https://github.com/psglinux/cmpe-272]](CMPE-272)
    - Using the base code as the boiler plate code for creating the infrastructure for CMPE-287

# Project
    This project aims to create an s/w infstratcure for **High Frequency and Low Latency Authentication at the Mobile Edge for 5G networks using uRLLC**. The idea of this porject is to enable a secure method of authentication at the mobile edge so that latency in communication of the IOT devices with the cloud servers could be reduced.
    - Any IOT devices that is authenticated would continue to remain authenticated for a configurable period of time.
    - The Authentication would happen at the Mobile Edge.
    - Mobile edge would not be storing the IOT device credential.
    - The cloud server would always be the supreme authority in authenticating a device.

## System Architecture

### Existing System Architecture
![Existing Architecture](https://github.com/psglinux/cmpe-287/blob/master/img/existing_arch.png)

![Proposed New Architecture](https://github.com/psglinux/cmpe-287/blob/master/img/new_arch.png)

## Software Architecture
### Assumptions
    1. We do not have any access to 5G Base Stations not 5G capable devices.
    2. 5G would be the **underlay protocol** with Overlay being MQTT.
    3. Simulating the Functionality using Containers on a Linux Host would demonstrate the Network Function Virtualization that is being eperimented.
    4. MQTT is the choice of protocol for IOT Devices. MQTT would be used for demonstrating the concept.

### MQTT Security
    1. MQTT client and Server should implement Authentication, Authorization and secure communication options. Applications concerned with critical infrastructure, personally identifiable information, or other personal or sensitive information are strongly advised to use these security capabilities.














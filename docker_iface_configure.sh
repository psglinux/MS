#!/bin/bash
ifconfig eth0 0
ifconfig eth1 0
brctl addbr snoopbr
brctl snoopbr addif eth0
brctl addif snoopbr eth0
brctl addif snoopbr eth1
ifconfig snoopbr 0
echo 'alert tcp any 5001 -> any any (msg:"iperf test";)' > /etc/suricata/rules/local.rules
sed -i s/" # - botcc.portgrouped.rules"/" - local.rules"/g /etc/suricata/suricata.yaml
service suricata start
# Don't let the script exit else it would cause the container to exit.
/bin/bash

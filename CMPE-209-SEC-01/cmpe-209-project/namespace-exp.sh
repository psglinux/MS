#!/bin/bash

#########################################
# variables start ->
#########################################

#network params
BR_IFACE=br0
NIC_IFACE=ens33
VETH0=veth0
VETH1=veth1

#operation vars
ADD=add
DEL=del
UP=up
DOWN=down
LO=lo
BR_IP_ADDR=192.168.213.133
BR_NET_MASK=255.255.255.0
ZERO_IP=0.0.0.0
DEF_GW=192.168.213.2

#namespace
HOSTAPP_NS=host-app
VETH1_IP_ADDR=192.168.213.253
VETH1_NET_MASK=255.255.255.0

EXT_IP=216.58.216.36
EXT_DOM=www.google.com
PING_COUNT=2

#########################################
# <- variables end 
#########################################

NS_ARR=($HOSTAPP_NS)

trace_func() {
    echo $@
}

#create/delete 2 name space in-com and host-app
# 1=add/del
add_del_ns() {
    ad=$1
    trace_func $0 "Adding Namespace" ${NS_ARR[@]}  
    for ns in ${NS_ARR[@]}; 
    do
        ip netns $ad $ns
    done
}

#bringup/down interface for the namespaces
updown_iface() {
    upd=$1
    ns=$2
    iface=$3
    ip netns exec $ns ip link set dev $iface $upd
}

# this would work only if both the namespace share the same iface name like lo
# updown_ns_iface $UP $LO
updown_ns_iface() {
    upd=$1
    iface=$2
    for ns in ${NS_ARR[@]}; 
    do
        updown_iface $upd $ns $iface
    done
}

#add the nic to the in-com name space
# takes 2 argument $1=namespace, $2=nic_iface_name
addnic_to_ns() {
    echo ""
}

#create a veth pair, 
# - veth-in-com - attached to the in-com namespace 
# - veth-host-app -attached to the host-app namespace
# takes 4 argument, 1=veth_name, 2=ns1 3=ns2
create_veth_pair() {
    echo ""
    ip link add $VETH0 type veth peer name $VETH1
    ifconfig $VETH0 $ZERO_IP up
    for ns in ${NS_ARR[@]};
    do
        ip link set $VETH1 netns $ns 
	#ip netns exec $ns ifconfig $VETH1 10.1.1.1/24 up
	ip netns exec $ns ifconfig $VETH1 $VETH1_IP_ADDR netmask $VETH1_NET_MASK up
    done
}

#setup linux bridge
# add a bridge add the $NIC_IFACE and $VETH0 to the bridge 
# add an ip interface in the bridge
create_def_ns_br() {
    brctl addbr $BR_IFACE
    ifconfig $NIC_IFACE $ZERO_IP up
    ifconfig $VETH0 $ZERO_IP up
    brctl addif $BR_IFACE $NIC_IFACE
    brctl addif $BR_IFACE $VETH0
    ifconfig $BR_IFACE $BR_IP_ADDR netmask $BR_NET_MASK up
}

#enable ip forwarding
enable_def_ns_ip_forward() {
    sysctl -w net.ipv4.ip_forward=1 
}

#set default route
set_def_ns_default_route() {
    ip route add default via $DEF_GW dev $BR_IFACE
}

#setup the bridge in the default namespace
setup_def_ns_br() {
    create_def_ns_br
    enable_def_ns_ip_forward
    set_def_ns_default_route
}

#reset to the original default g/w

restart_networking() {
    sysctl -w net.ipv4.ip_forward=0 
    systemctl restart networking
}
reset_default_iface_config() {
    ifconfig $NIC_IFACE $BR_IP_ADDR up
    #ip route add default via $DEF_GW dev $NIC_IFACE
    restart_networking
}

#delete bridge configuration
del_br() {
    brctl delif $BR_IFACE $NIC_IFACE 
    brctl delif $BR_IFACE $VETH0
    ifconfig br0 down
    brctl delbr $BR_IFACE
}


# show the ns configuration 
show_ns() {
    echo "Default namespace info :"
    ifconfig -a
    ip link show
    bridge fdb show
    arp -a
    ip neighbor
    ip route
    iptables -L
    echo ""
    for ns in ${NS_ARR[@]}; 
    do
        echo "links for namespace "$ns:
	ip netns exec $ns ifconfig -a 
	ip netns exec $ns ip link show
	ip netns exec $ns bridge fdb show 
	ip netns exec $ns arp -a
	ip netns exec $ns ip neighbor 
	ip netns exec $ns ip route 
	ip netns exec $ns iptables -L
        echo ""
    done
}

#test the ns configruation
# test0: ping from BR_IFACE to GOOG
# test1 : ping from VETH1 to BR_IFACE
# test2 : ping from VETH1 to GOOG 

test_ns_setup() {
    ip netns exec $HOSTAPP_NS ping $VETH1_IP_ADDR -c $PING_COUNT
    ip netns exec $HOSTAPP_NS ping $BR_IP_ADDR -c $PING_COUNT
    ping $DEF_GW -I $BR_IFACE -c $PING_COUNT
    ip netns exec $HOSTAPP_NS ping $DEF_GW -c $PING_COUNT
    ping $EXT_DOM -I $BR_IFACE -c $PING_COUNT
    #ip netns exec $HOSTAPP_NS ping $EXT_DOM -c $PING_COUNT
    ip netns exec $HOSTAPP_NS ping $EXT_IP -c $PING_COUNT
}

# test to check if all the configurations are removed
test_clean_up() {
    ping $DEF_GW -I $NIC_IFACE -c $PING_COUNT
    ping $EXT_DOM -I $NIC_IFACE -c $PING_COUNT
}


usage() { echo "Usage: $0 [-c] [-d] [-s] [-t] [T]" 1>&2; exit 1; }

while getopts ":cdstT" o; do
    case "${o}" in
        c)
            c=${OPTARG}
	    echo "create"
	    add_del_ns $ADD 
            updown_ns_iface $UP $LO
	    create_veth_pair
	    setup_def_ns_br
	    break
            ;;
        d)
            d=${OPTARG}
	    echo "delete"
	    del_br
	    add_del_ns $DEL 
	    reset_default_iface_config
	    break
            ;;
        s)
            s=${OPTARG}
	    echo "show config"
	    show_ns
	    break
            ;;
        t)
            t=${OPTARG}
	    echo "testing the setup"
	    test_ns_setup
	    break
            ;;
        T)
            t=${OPTARG}
	    echo "testing the cleanup setup"
	    test_clean_up
	    break
            ;;
        *)
            usage
            ;;
    esac
done
#shift $((OPTIND-1))


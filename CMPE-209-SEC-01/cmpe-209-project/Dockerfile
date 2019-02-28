#
# Ubuntu Dockerfile
#
# https://github.com/dockerfile/ubuntu
#

# Pull base image.
FROM ubuntu:18.04

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y software-properties-common && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  apt-get install -y net-tools && \
  apt-get install -y ethtool && \
  apt-get install -y bridge-utils && \
  apt-get install -y iproute2 && \
  apt-get install -y iputils-ping && \
  apt-get install -y strace && \
  apt-get install -y tcpdump && \
  add-apt-repository ppa:oisf/suricata-stable && \
  apt-get install -y libpcre3-dbg libpcre3-dev autoconf automake libtool libpcap-dev libnet1-dev libyaml-dev libjansson4 libcap-ng-dev libmagic-dev libjansson-dev zlib1g-dev && \
  apt-get install -y libnetfilter-queue-dev libnetfilter-queue1 libnfnetlink-dev && \
  apt-get install suricata suricata-dbg -y && \
  rm -rf /var/lib/apt/lists/*

# Add files.
COPY ./start.sh /root/start.sh

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

# Define default command.
#CMD ["bash"]

# ENTRY PONIT
ENTRYPOINT ["./start.sh"]

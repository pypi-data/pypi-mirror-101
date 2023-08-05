#!/bin/sh
echo "Seeding /dev/random"
haveged -f /dev/random
dockerd --iptables=false  >> /var/log/dockerd.log &
biolib listen --enclave

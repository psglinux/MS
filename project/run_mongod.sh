#!/bin/bash
DBPATH=$1
if [ "x${DBPATH}" == "x" ]; then
	DBPATH=~/clala-git/cmpe-272/project/data
fi
mongod --dbpath ${DBPATH} -vvv --syslog > /tmp/db.txt 2>&1 &


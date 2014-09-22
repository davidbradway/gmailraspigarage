#!/bin/bash
service raspigmail.sh status| grep FAIL > /dev/null 2>&1
if [ $? != 0 ]
then
    echo "Still running"
    sudo service raspigmail.sh status
else
    echo "FAILED"
    sudo service raspigmail.sh start
fi

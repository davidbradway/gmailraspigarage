#!/bin/bash
service raspigmail.sh status| grep 'raspigmail.sh start/running' > /dev/null 2>&1
if [ $? != 0 ]
then
    echo "then"
    sudo service raspigmail.sh status
else
    echo "else"
    sudo service raspigmail.sh start
fi

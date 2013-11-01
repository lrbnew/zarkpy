#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

rev1="$1"

if [ "x${rev1}" != "xexp" ] && [ "x${rev1}" != "xmaster" ]; then
    echo "Usage: $(basename $0) {master|exp} "
    exit 1
fi

cd /opt/git/homework.git
git archive master -o /tmp/homework.tgz
ret=$?
if [ "x${ret}" != "x0" ]; then
    echo "An error occurs when archiving."
    exit 1
fi

if [ "${rev1}"="master" ]; then

    mkdir -p /opt/homework
    cd /opt/homework
    tar xf /tmp/homework.tgz

    cp /opt/homework/conf/nginx/master /etc/nginx/sites-available/homework-master
    ln -s /etc/nginx/sites-available/homework-master /etc/nginx/sites-enabled/homework-master
    nginx -t
    ret=$?
    if [ "x${ret}" != "x0" ]; then
        echo "An error occurs when check nginx -t"
        exit 1
    fi
    /etc/init.d/nginx reload

    echo "Please type mysql root password:"
    mysql -uroot -p  --default-character-set=utf8 < /opt/homework/doc/sql/init_database.sql

    sh /opt/homework/tool/export.sh master


elif [ "${rev1}"="exp" ]; then
    mkdir -p /opt/homework_exp
    cd /opt/homework_exp
    tar xf /tmp/homework.tgz

    cp /opt/homework_exp/conf/nginx/exp /etc/nginx/sites-available/homework-exp
    ln -s /etc/nginx/sites-available/homework-exp /etc/nginx/sites-enabled/homework-exp
    nginx -t
    ret=$?
    if [ "x${ret}" != "x0" ]; then
        echo "An error occurs when nginx -t"
        exit 1
    fi
    /etc/init.d/nginx reload

    sh /opt/homework_exp/tool/export.sh exp

fi

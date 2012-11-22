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

cd /opt/git/zarkpy.git
git archive master -o /tmp/zarkpy.tgz
ret=$?
if [ "x${ret}" != "x0" ]; then
    echo "An error occurs when archiving."
    exit 1
fi

if [ "${rev1}"=="master" ]; then

    mkdir -p /opt/zarkpy
    cd /opt/zarkpy
    tar xf /tmp/zarkpy.tgz

    cp /opt/zarkpy/conf/nginx/master /etc/nginx/sites-available/zarkpy-master
    ln -s /etc/nginx/sites-available/zarkpy-master /etc/nginx/sites-enabled/zarkpy-master
    nginx -t
    ret=$?
    if [ "x${ret}" != "x0" ]; then
        echo "An error occurs when check nginx -t"
        exit 1
    fi
    /etc/init.d/nginx reload

    echo "Please type mysql root password:"
    mysql -uroot -p  --default-character-set=utf8 < /opt/zarkpy/doc/sql/init_database.sql

    sh /opt/zarkpy/tool/export.sh master


elif [ "${rev1}"=="exp" ]; then
    mkdir -p /opt/zarkpy_exp
    cd /opt/zarkpy_exp
    tar xf /tmp/zarkpy.tgz

    cp /opt/zarkpy_exp/conf/nginx/exp /etc/nginx/sites-available/zarkpy-exp
    ln -s /etc/nginx/sites-available/zarkpy-exp /etc/nginx/sites-enabled/zarkpy-exp
    nginx -t
    ret=$?
    if [ "x${ret}" != "x0" ]; then
        echo "An error occurs when nginx -t"
        exit 1
    fi
    /etc/init.d/nginx reload

    sh /opt/zarkpy_exp/tool/export.sh exp

fi

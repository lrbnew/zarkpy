#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

cp /opt/homework/conf/nginx/master /etc/nginx/sites-enabled/homework
/etc/init.d/nginx restart

echo "127.0.0.1 me.homework.com" >> /etc/hosts

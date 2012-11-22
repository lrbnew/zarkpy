#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

cp /opt/zarkpy/conf/nginx/master /etc/nginx/sites-enabled/zarkpy
/etc/init.d/nginx restart

echo "127.0.0.1 me.zarkpy.com" >> /etc/hosts

#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

aptitude install git
aptitude install gcc
aptitude install nginx
aptitude install spawn-fcgi
aptitude install python-webpy
aptitude install python-httplib2

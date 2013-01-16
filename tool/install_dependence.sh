#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

aptitude update
aptitude install locales
dpkg-reconfigure locales

aptitude install git
aptitude install gcc
aptitude install nginx
aptitude install mysql-client
aptitude install mysql-server 
aptitude install spawn-fcgi

aptitude install python-webpy
aptitude install python-httplib2
aptitude install python-mysqldb
aptitude install python-setuptools
aptitude install python-imaging
aptitude install python-memcache
easy_install pip

aptitude install sphinxsearch
aptitude install imagemagick 
aptitude install memcached 
aptitude install exim4
aptitude install heirloom-mailx

aptitude install curl vnstat vim zsh unzip dstat telnet

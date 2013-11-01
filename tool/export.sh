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
git archive ${rev1} -o /tmp/homework.tgz
ret=$?
if [ "x${ret}" != "x0" ]; then
    echo "An error occurs when archiving."
    exit 1
fi

if [ "${rev1}" = "master" ]; then
    cd /opt/homework
elif [ "${rev1}" = "exp" ]; then
    cd /opt/homework_exp
fi

tar xf /tmp/homework.tgz

if [ "${rev1}" = "master" ]; then
    sed -i "s/#\s*web.config.debug\s*=\s*False/web.config.debug = False/"  /opt/homework/web/cgi/app.py
    sed -i "s/'HOST_NAME'\s*:\s*'http:\/\/me.homework.com'/'HOST_NAME' : 'http:\/\/homework.com'/"  /opt/homework/web/cgi/site_helper.py
    chown www-data:www-data -R /opt/homework
    python /opt/homework/web/cgi/processor/file_version.py inc
    /opt/homework/tool/launch.sh restart

elif [ "${rev1}" = "exp" ]; then
    sed -i "s/#\s*web.config.debug\s*=\s*False/web.config.debug = False/"  /opt/homework_exp/web/cgi/app.py
    sed -i "s/'HOST_NAME'\s*:\s*'http:\/\/me.homework.com'/'HOST_NAME' : 'http:\/\/exp.homework.com'/"  /opt/homework_exp/web/cgi/site_helper.py
    sed -i "s/'APP_ROOT_PATH'\s*:\s*'\/opt\/homework\/'/'APP_ROOT_PATH' : '\/opt\/homework_exp\/'/"  /opt/homework_exp/web/cgi/site_helper.py
    sed -i "s/'APP_PORT'\s*:\s*10120/'APP_PORT' : 10121/" /opt/homework_exp/web/cgi/site_helper.py
    sed -i "s/'SESSION_PATH'\s*:\s*'\/opt\/homework\/session\/'/'SESSION_PATH' : '\/opt\/homework_exp\/session\/'/"  /opt/homework_exp/web/cgi/site_helper.py
    sed -i "s/'ERROR_LOG_PATH'\s*:\s*'\/opt\/homework\/log\/error.log'/'ERROR_LOG_PATH' : '\/opt\/homework_exp\/log\/error.log'/"  /opt/homework_exp/web/cgi/site_helper.py
    chown www-data:www-data -R /opt/homework_exp
    /opt/homework_exp/tool/launch-exp.sh restart

fi

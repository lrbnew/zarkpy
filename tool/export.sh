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
git archive ${rev1} -o /tmp/zarkpy.tgz
ret=$?
if [ "x${ret}" != "x0" ]; then
    echo "An error occurs when archiving."
    exit 1
fi

if [ "${rev1}"=="master" ]; then
    cd /opt/zarkpy
elif [ "${rev1}"=="exp" ]; then
    cd /opt/zarkpy_exp
fi

tar xf /tmp/zarkpy.tgz

if [ "${rev1}"=="master" ]; then
    sed -i "s/#\s*web.config.debug\s*=\s*False/web.config.debug = False/"  /opt/zarkpy/web/cgi/app.py
    sed -i "s/'HOST_NAME'\s*:\s*'http:\/\/me.zarkpy.com'/'HOST_NAME' : 'http:\/\/zarkpy.com'/"  /opt/zarkpy/web/cgi/site_helper.py
    python /opt/zarkpy/web/cgi/site_helper.py init_dir
    chown www-data:www-data -R /opt/zarkpy
    /opt/zarkpy/tool/launch.sh restart

elif [ "${rev1}"=="exp" ]; then
    sed -i "s/#\s*web.config.debug\s*=\s*False/web.config.debug = False/"  /opt/zarkpy_exp/web/cgi/app.py
    sed -i "s/'HOST_NAME'\s*:\s*'http:\/\/me.zarkpy.com'/'HOST_NAME' : 'http:\/\/exp.zarkpy.com'/"  /opt/zarkpy_exp/web/cgi/site_helper.py
    sed -i "s/'APP_ROOT_PATH'\s*:\s*'\/opt\/zarkpy\/'/'APP_ROOT_PATH' : '\/opt\/zarkpy_exp\/'/"  /opt/zarkpy_exp/web/cgi/site_helper.py
    sed -i "s/'APP_PORT'\s*:\s*10000/'APP_PORT' : 10001/" /opt/zarkpy_exp/web/cgi/site_helper.py
    sed -i "s/'SESSION_PATH'\s*:\s*'\/opt\/zarkpy\/session'/'SESSION_PATH' : '\/opt\/zarkpy_exp\/session'/"  /opt/zarkpy_exp/web/cgi/site_helper.py
    sed -i "s/'ERROR_LOG_PATH'\s*:\s*'\/opt\/zarkpy\/log\/error.log'/'ERROR_LOG_PATH' : '\/opt\/zarkpy_exp\/log\/error.log'/"  /opt/zarkpy_exp/web/cgi/site_helper.py
    python /opt/zarkpy_exp/web/cgi/site_helper.py init_dir
    chown www-data:www-data -R /opt/zarkpy_exp
    /opt/zarkpy_exp/tool/launch-exp.sh restart

fi

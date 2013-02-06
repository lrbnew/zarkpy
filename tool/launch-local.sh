#!/bin/bash
case $1 in
    "start")
        spawn-fcgi -f "/opt/zarkpy/web/cgi/app.py" -d "/opt/zarkpy/web/cgi" -a 127.0.0.1 -p 10000 -F 1
        exit ${ret}
        ;;
    "stop")
        ps x | grep app.py | grep python | grep zarkpy | awk '{print $1}' | xargs kill
        ;;
    "restart")
        $0 stop
        $0 start
        ;;
    *)
        echo "usage: $(basename $0) {start|stop|restart}"
        exit 1
        ;;
esac

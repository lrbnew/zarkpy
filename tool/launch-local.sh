#!/bin/bash
ps x | grep app.py | grep python | grep zarkpy | awk '{print $1}' | xargs kill
spawn-fcgi -f "/opt/zarkpy/web/cgi/app.py" -d "/opt/zarkpy/web/cgi" -a 127.0.0.1 -p 10000 -F 1

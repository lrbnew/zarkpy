#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

cd /opt/git/homework.git
git config --add core.sharedRepositoy group
chgrp  -R homeworkdev /opt/git/homework.git
chmod g+rsw -R /opt/git/homework.git
echo "#!/bin/sh\n chgrp -R homeworkdev . 2>/dev/null" > /opt/git/homework.git/hooks/post-update
chmod g+x /opt/git/homework.git/hooks/post-update

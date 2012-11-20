#!/bin/bash
if [ "x$(whoami)" != "xroot" ]; then
    echo "Only root can run this script."
    exit 1
fi

cd /opt/git/zarkpy.git
git config --add core.sharedRepositoy group
chgrp  -R zarkpydev /opt/git/zarkpy.git
chmod g+rsw -R /opt/git/zarkpy.git
echo "#!/bin/sh\n chgrp -R zarkpydev . 2>/dev/null" > /opt/git/zarkpy.git/hooks/post-update
chmod g+x /opt/git/zarkpy.git/hooks/post-update

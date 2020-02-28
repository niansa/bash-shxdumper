#! /bin/bash

if [ "$(whoami)" != "root" ]; then
    echo "Can not run without root privileges!"
    exit 1
elif [ "$2" = "" ]; then
    echo "Usage: quickuse.sh <input> <output>"
    exit 1
fi

if ! (ls /bin/bash-shxdumper1 2> /dev/null); then
    echo ""
    echo "Running preinstallation... This step is done the first time this script runs on this machine only!"
    echo ""
    oldpwd="$(pwd)"
    cd /tmp &&
    rm -rf ./shxdumper &&
    git clone https://github.com/niansa/bash-shxdumper shxdumper ||
    exit
    cd shxdumper
    ./configure &&
    make -j2 ||
    exit
    cp ./bash /bin/bash-shxdumper1
    cd "$oldpwd"
fi
mv /bin/bash /bin/bash.bak && cp /bin/bash-shxdumper1 /bin/bash

OUTFILE="$2" timeout 1s bash -c "$1"
echo "Filecreated: $2"


echo -n "Cleaning up..."
cd /tmp/
rm -rf ./shxdumper 2> /dev/null
rm /bin/bash
mv /bin/bash.bak /bin/bash
chmod a+x /bin/bash
echo "Done"

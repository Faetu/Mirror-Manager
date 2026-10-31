#!/bin/bash

echo "check for module 'requests'"
moduleInstalled=$(pip freeze --local | grep requests)

if [ -z "${moduleInstalled}" ]
then
    echo "install requests with pip"
    sudo $1/bin/pip install requests
else
    echo "no need to install requests module"
fi

echo "copy mirman to /usr/bin/"
cp ./mirman /usr/bin/
echo "copy Available_Countries.json file to /usr/bin/"
cp ./Available_Countries.json /usr/bin/

echo "make mirman executable"
sudo chmod +x /usr/bin/mirman
#!/usr/bin/env bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

GIT_DIRECTORY=/var/www/hackfsu_com
SYSTEMD_SERVICE=hackfsu-com

set -x

# Go to the git directory on the server
cd ${GIT_DIRECTORY}

# Turn off service
systemctl stop ${SYSTEMD_SERVICE}

# Pull from git and make sure on a fresh live branch
git fetch --all
git reset --hard
git checkout live
git reset --hard origin/live

# Update dependencies
./venv/bin/pip3.5 install -r ./requirements.txt
npm install
npm run build

systemctl start ${SYSTEMD_SERVICE}
systemctl status ${SYSTEMD_SERVICE}

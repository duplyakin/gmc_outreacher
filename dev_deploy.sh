#!/bin/bash
set -e

cp -f ./init_scripts/o24-dev.service /etc/systemd/system/
chown root:root /etc/systemd/system/o24-dev.service
chmod 755 /etc/systemd/system/o24-dev.service
systemctl enable o24-dev

cp -f ./init_scripts/dv.outreacher24.com /etc/nginx/sites-available/
ln -fs /etc/nginx/sites-available/dv.outreacher24.com /etc/nginx/sites-enabled

cp -f ./init_scripts/mongod.conf /etc/
cp -f ./init_scripts/mongod.service /etc/systemd/system/
chmod 755 /etc/systemd/system/mongod.service

systemctl enable mongod

systemctl daemon-reload
systemctl start mongod
systemctl start o24-dev
systemctl restart nginx

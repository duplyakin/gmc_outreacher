#!/bin/bash
set -e

cp -f ./init_scripts/prod/o24-prod.service /etc/systemd/system/
chown root:root /etc/systemd/system/o24-prod.service
chmod 755 /etc/systemd/system/o24-prod.service


cp -f ./init_scripts/prod/app.outreacher24.com /etc/nginx/sites-available/
ln -fs /etc/nginx/sites-available/app.outreacher24.com /etc/nginx/sites-enabled

cp -f ./init_scripts/mongod.conf /etc/
cp -f ./init_scripts/mongod.service /etc/systemd/system/
chmod 755 /etc/systemd/system/mongod.service

systemctl enable o24-prod
systemctl enable mongod

systemctl daemon-reload
systemctl start mongod
systemctl start o24-prod
systemctl restart nginx

#!/bin/bash
set -e

cp -f ./init_scripts/prod/o24-prod.service /etc/systemd/system/
chown root:root /etc/systemd/system/o24-prod.service
chmod 755 /etc/systemd/system/o24-prod.service


cp -f ./init_scripts/prod/app.outreacher24.com /etc/nginx/sites-available/
ln -fs /etc/nginx/sites-available/app.outreacher24.com /etc/nginx/sites-enabled

cp -f ./init_scripts/prod/mongod.conf /etc/
cp -f ./init_scripts/prod/mongod.service /etc/systemd/system/
chmod 755 /etc/systemd/system/mongod.service

cp -f ./init_scripts/prod/celeryd.conf /etc/
cp -f ./init_scripts/prod/celery-beat.service /etc/systemd/system/
cp -f ./init_scripts/prod/celery-o24-worker.service /etc/systemd/system/

chmod 755 /etc/systemd/system/celery-beat.service
chmod 755 /etc/systemd/system/celery-o24-worker.service


systemctl enable o24-prod
systemctl enable mongod
systemctl enable celery-beat
systemctl enable celery-o24-worker

systemctl daemon-reload
systemctl start mongod
systemctl start o24-prod
systemctl restart nginx

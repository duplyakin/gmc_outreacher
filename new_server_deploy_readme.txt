В o24 поддерживаем requirements.txt:
pipreqs --force --encoding=utf8 .   //Make this command from o24 folder
НЕ
pip freeze > requirements.txt

Структура папок:
~/o24_dev/ - здесь лежит master, используем для dev версии
~/o24_prod/ - здесь лежит tag: prod_v_X.X, используем для prod версии

Установка nginx:
sudo apt-get install nginx

Создаем virtualenv
cd {project_folder}
virtualenv -p python3.7 ./.venv
source ./.venv/bin/activate
pip install -r o24/requirements.txt

Ставим сервер:
pip install gunicorn

#deploy vue.js
Стаим node последней версии
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs


#Install reddis
sudo apt-get install redis-server
redis-cli ping
sudo systemctl enable redis-server.service
pip install -U "celery[redis]"

Добавляем сертификат:
sudo add-apt-repository ppa:certbot/certbot
sudo apt install python-certbot-nginx
sudo certbot --nginx -d outreacher24.com -d dv.outreacher24.com -d app.outreacher24.com -d via.outreacher24.com

 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/outreacher24.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/outreacher24.com/privkey.pem
   Your cert will expire on 2020-08-12. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:


#CREATE PRODUCTION TEST DATA
APP_ENV=Production python -m unittest discover -s ./o24/production_tests/ -p "*test_production_database.py"

#create production database
python -m unittest discover test_data_production -s .\o24\deployment_scripts\ -p "*deploy_data_to_database.py"


#load Production google apps cookie
APP_ENV=Production python -m o24.migrations.update_google_settings prod


#deploy FLOWER to monitor celery
pip install flower

#setup Password for flower in nginx
sudo sh -c "echo -n 'flower:' >> /etc/nginx/.htpasswd"
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/.htpasswd"

#Install nodejs services - pm2 is a manager
sudo npm install -g pm2

#Install global bs dependencies
cd /home/o24user/o24_prod/bs
sudo npm install -g
pm2 start app/server.js

#Install global crawler dependencies
cd /home/o24user/o24_prod/crawlers
sudo npm install -g
pm2 start init.js

# сохраняем список сервисов
pm2 save
pm2 unstartup

#GENERATE PM2 systemd script (details: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-node-js-application-for-production-on-ubuntu-16-04)
pm2 startup systemd
sudo ТО ЧТО сгенерировали
добавить APP_ENV=Production в /etc/systemd/system/pm2-o24user.service

#Логи от PM2 лежат здесь:
~/.pm2/logs/

#deploy scripts to production
sudo ./prod_deploy.sh

#INSTALL chrome
cd /home/o24user/headless_chromium
npm install puppeteer
#create symlinks
sudo ln -s /home/o24user/headless_chromium/node_modules/puppeteer/.local-chromium /home/o24user/o24_prod/bs/node_modules/puppeteer/.local-chromium
sudo ln -s /home/o24user/headless_chromium/node_modules/puppeteer/.local-chromium /home/o24user/o24_prod/crawlers/node_modules/puppeteer/.local-chromium
sudo apt-get install -y libgbm-dev


#VIEW SYSTEMCTL ERRORS:
journalctl -xe

#CHECK IF nodejs packgae installed
npm list puppeter

#МОНИТОРИНГ ВСЕГО
systemctl status pm2-o24user
systemctl status mongod
systemctl status o24-prod
systemctl status celery-beat
systemctl status celery-o24-worker
systemctl status nginx
systemctl status flower-monitor

#Рестарт основного
sudo systemctl stop o24-prod
sudo systemctl stop celery-beat
sudo systemctl stop celery-o24-worker
sudo systemctl stop flower-monitor

sudo systemctl start o24-prod
sudo systemctl start celery-beat
sudo systemctl start celery-o24-worker
sudo systemctl start flower-monitor
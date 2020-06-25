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


#deploy scripts to production
sudo ./prod_deploy.sh

#VIEW SYSTEMCTL ERRORS:
journalctl -xe
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
gunicorn -b localhost:8880 -w 4 o24.wsgi:app #test gunicorn
gunicorn -c gunicorn_config_dev.py -e APP_ENV=Test o24.wsgi:app


Добавляем сертификат:
sudo add-apt-repository ppa:certbot/certbot
sudo apt install python-certbot-nginx
sudo certbot --nginx -d outreacher24.com -d dv.outreacher24.com

 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/outreacher24.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/outreacher24.com/privkey.pem
   Your cert will expire on 2020-08-12. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:


#deploy vue.js
Стаим node последней версии
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install -y nodejs

В o24 поддерживаем requirements.txt:
pipreqs --encoding=utf8 .   //Make this command from o24 folder
НЕ
pip freeze > requirements.txt

Структура папок:
~/o24_dev/ - здесь лежит master, используем для dev версии
~/o24_prod/ - здесь лежит tag: prod_v_X.X, используем для prod версии

Создаем virtualenv
cd {project_folder}
virtualenv -p python3.7 ./.venv
source ./.venv/bin/activate
pip install -r o24/requirements.txt

Ставим сервер:
pip install gunicorn
gunicorn -b localhost:8880 -w 4 o24.wsgi:app #test gunicorn
gunicorn -c gunicorn_config_dev.py -e APP_ENV=Test o24.wsgi:app
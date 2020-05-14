В o24 поддерживаем requirements.txt:
pipreqs --encoding=utf8 .   //Make this command from o24 folder
НЕ
pip freeze > requirements.txt

Структура папок:
~/o24_dev/ - здесь лежит master, используем для dev версии
~/o24_prod/ - здесь лежит tag: prod_v_X.X, используем для prod версии


#unittest docs:
https://realpython.com/python-testing/

#Setup TEST Envirnment
$env:APP_ENV="Test"


#execute all tests in a folder:
python -m unittest discover -s .\o24\tests\
python -m unittest discover -s .\o24\tests\ -p "*db_entities.py"

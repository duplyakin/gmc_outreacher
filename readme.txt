#unittest docs:
https://realpython.com/python-testing/

#Setup TEST Envirnment
$env:APP_ENV="Test"


#execute all tests in a folder:
python -m unittest discover -s .\o24\tests\
python -m unittest discover -s .\o24\tests\ -p "*db_entities.py"


#which tasks use with celery:
https://www.toptal.com/python/orchestrating-celery-python-background-jobs

#call celery tasks:
task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})

#task signature:
task.s(arg1, arg2, kwarg1='x', kwargs2='y').apply_async()

#no need to have app context, use @shared_task:
http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-the-shared-task-decorator

#start celery worker
#logic explained here: https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern
celery -A o24.backend.handlers.worker_start.celery worker -E -l info -P gevent
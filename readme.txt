#unittest docs:
https://realpython.com/python-testing/

#Setup TEST Envirnment
$env:APP_ENV="Test"


#execute all tests in a folder:
python -m unittest discover -s .\o24\tests\

python -m unittest discover -s .\o24\tests\ -p "*db_entities.py"
python -m unittest o24.tests.test_scheduler_campaigns.TestScheduler.test_1_start_campaign



python -m unittest discover -s .\o24\tests\ -p "*mongo_test_lookup.py"


python -m unittest discover -s .\o24\tests\ -p "*mongo_updates.py"
python -m unittest discover -s .\o24\tests\ -p "*test_scheduler_campaigns.py"
python -m unittest discover -s .\o24\tests\ -p "*test_scheduler_loop.py"


python -m unittest o24.tests.test_scheduler.TestScheduler.test_7_scheduler_loop
python -m unittest o24.tests.test_mongo_updates.TestBulkUpdates.test_5_taskqueue_methods

python -m unittest o24.tests.test_db_entities
python -m unittest o24.tests.test_scheduler


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
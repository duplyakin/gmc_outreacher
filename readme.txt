#unittest docs:
https://realpython.com/python-testing/

#Setup TEST Envirnment
$env:APP_ENV="Test"

python -m o24.tests.run_flask_server

#execute all tests in a folder:
python -m unittest discover -s .\o24\tests\

python -m unittest discover -s .\o24\tests\ -p "*db_entities.py"
python -m unittest o24.tests.test_scheduler_campaigns.TestScheduler.test_1_start_campaign


python -m unittest discover -s .\o24\tests\ -p "*test_gmail_send.py"


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


#SOLUTION for flagged emails:
https://stackoverflow.com/questions/56548494/emails-sent-using-gmail-api-are-being-flagged-as-phishy-by-gmail
"Emails sent using Gmail API are being flagged as phishy by Gmail"
https://mediatemple.net/community/products/googleapps/204645590/configuring-the-%22send-mail-as%22-feature-in-g-suite
https://developers.google.com/gmail/imap/xoauth2-protocol - SMTP Oauth authentication
https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py - SMTP python usage example

<img width=3D"1" height=3D"1" style=3D"display: block;" alt=3D"" src=3D"h=
ttps://via.smartreach-mail.com/ot2/ge2tgnbxhe3dk=3D=3D=3D/open">

Send with images:
https://stackoverflow.com/questions/19171742/send-e-mail-to-gmail-with-inline-image-using-python

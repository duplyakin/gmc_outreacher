
#HOW to launch server to test frontend
python 3.7, pip 19.2.3

#Monitoring scripts
python -m o24.monitoring.taskqueue

celery flower -A o24.backend.handlers.worker_start.celery --address=127.0.0.1 --port=5555

0. Запускаем монгу (на винде):
идем сюда: C:\Program Files\MongoDB\Server\4.2\bin
в командной строке: ./mongod -f ./mongod.cfg

$env:APP_ENV="Production"

Все шаги делаем из корня: mc_outreacher\
1. Устанвливаем тестовую переменную окружения (!!!)
$env:APP_ENV="Test"
SET APP_ENV=Test

2. Создаем базу с тестоваыми данными:
python -m unittest discover test_data -s .\o24\production_tests\ -p "*1_models.py"
py -m unittest discover test_data -s .\o24\production_tests\ -p "*1_models.py"
py -m unittest discover test_data_production -s .\o24\production_tests\ -p "*1_models.py"

3. Запускаем тестовый сервер
python -m o24.tests.run_flask_server
py -m o24.tests.run_flask_server


ПОСЛЕ ЭТОГО запускаем фронтенд:
4. Идем в mc_outreacher\frontend
5. Запускаем фронтенд:
npm run dev


Если не установлен модуль для питона, то в корне: mc_outreacher\ 
6. pip install <module_name>

7. Запускаем все production tests

python -m unittest discover -s .\o24\tests\production_tests\

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
python -m unittest discover -s .\o24\tests\ -p "*test_gmail_provider_headers.py"

python -m unittest discover -s .\o24\tests\ -p "*test_gmail_handlers.py"

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

How Gmail threading works:
http://www.sensefulsolutions.com/2010/08/how-does-email-threading-work-in-gmail.html



How to work with images:
    def create_multipart_message(self, 
                                email_from, 
                                email_to, 
                                subject, 
                                html_version, 
                                plain_version,
                                thread_id=None,
                                msgId=None,
                                image_data=None):
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['subject'] = subject
        msgRoot['from'] = email_from
        msgRoot['to'] = email_to
        if msgId:
            msgRoot.add_header('Reference', msgId)
            msgRoot.add_header('In-Reply-To', msgId)


        #msgRoot.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(plain_version, 'plain', 'utf-8')
        msgAlternative.attach(msgText)

        msg_html = None
        if image_data:
            msg_html = MIMEText(html_version.format(alt=html.escape(image_data['title'], quote=True), 
                                                cid=image_data['cid']), 'html', 'utf-8')
        else:
            msg_html = MIMEText(html_version, 'html', 'utf-8')

        msgAlternative.attach(msg_html)
        
        if image_data:
            msg_image = MIMEImage(image_data.get('raw'))
            msg_image.add_header('Content-ID', '<{}>'.format(image_data['cid']))
            msgRoot.attach(msg_image)

        raw_message = {'raw': base64.urlsafe_b64encode(msgRoot.as_string().encode()).decode()}
        if thread_id:
            raw_message['threadId'] = thread_id
        
        return raw_message


https://github.com/charlierguo/gmail/blob/master/gmail/gmail.py

Use to search messages: rfc822msgid:9db8b174-b5f7-8253-8c79-defc35f68443@mixmax.com 
https://developers.google.com/gmail/api/guides/filtering

Generate your own message-ID
https://stackoverflow.com/questions/22939035/how-to-get-message-id-of-email-sent-from-smtplib

Peoples API:
https://developers.google.com/people/v1/read-people

SMTP Rfc:
https://tools.ietf.org/html/rfc2822

How to encode messages:
https://en.wikipedia.org/wiki/Quoted-printable

https://stackoverflow.com/questions/31433633/reply-to-email-using-python-3-4/31513615#31513615?newreg=35dfc90756ce4400a91687718a134d39

https://github.com/tausen/mu4e-mimelook/blob/master/mimelook.py

Попробовать вот это:
https://wordeology.com/computer/how-to-send-good-unicode-email-with-python.html

Tests for Flask_user:
https://github.com/lingthio/Flask-User/blob/a379fa0a281789618c484b459cb41236779b95b1/flask_user/tests/test_roles.py#L67


Vue bootstrap project structure documentation:
http://vuejs-templates.github.io/webpack/

All vue API methods (like derictives) here:
https://vuejs.org/v2/api/#Options-Data

VUE discord community:
https://discordapp.com/channels/325477692906536972/568340117052456970


Vue.js authentication:
https://www.reddit.com/r/flask/comments/e0gtuf/how_to_implement_authentication_when_using_flask/

#Mongo
C:\Program Files\MongoDB\Server\4.2\bin
./mongod -f ./mongod.cfg

#Test Json requests with this:
https://chrome.google.com/webstore/detail/advanced-rest-client/hgmloofddffdnphfgcellkdfbfbjeloo/related

#Flask Mongo Rest-API:
https://dev.to/paurakhsharma/flask-rest-api-part-1-using-mongodb-with-flask-3g7d

#Vuejs github
https://github.com/vuejs/vue/tree/6fe07ebf5ab3fea1860c59fe7cdd2ec1b760f9b0

#element-ui el-select source code:
https://github.com/ElemeFE/element/blob/3270276c3c1b7e477ca65b6b7e2f5015e6baa92e/packages/select/src/select.vue


#JWT Auth
https://github.com/AngCosmin/flask-vue-auth/blob/master/vue/src/api/axios-auth.js

https://testdriven.io/blog/deploying-flask-to-heroku-with-docker-and-gitlab/

https://dev.to/pacheco/how-to-dockerize-a-node-app-and-deploy-to-heroku-3cch

https://www.reddit.com/r/docker/comments/9q6lkn/the_best_way_to_dockerize_webapplication/

https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application


VUEJS login and register tutorial:
https://jasonwatmore.com/post/2018/07/14/vue-vuex-user-registration-and-login-tutorial-example
https://github.com/cornflourblue/vue-vuex-registration-login-example - example of login register app


Список сервисов, которые запускаются:
Celery beat - планировщик celery, который выполняет периодические задачи. Без его запуска периодические задачи не будут работать.
    celery -A o24.backend.handlers.worker_start.celery beat

Scheduler (celery) - отвечает за обработку задач в TaskQueue. Запускается через emit_cheduler. Запускается по крону каждые config.SCHEDULER_HANDLER_PERIOD (сейчас это 60 секунду)
Enricher (celery) - выполняет задачи поиска емайлов. Задачи лежат в очереди . Запускается через emit_enricher (celery). Запускается по крону каждые config.ENRICHER_HANDLER_PERIOD (сейчас это 120 секунд).

    celery -A o24.backend.handlers.worker_start.celery worker -E -l info -P gevent



Linkedin handlers (nodejs) - выполняет linkedin action’ы из очереди. Запускается из crawlers/init.js
    node init.js
BS service (nodejs) - должен решать блокировки с Linkedin. Запускается из BS/app/server.js
    node server.js


#google developer console - to CHANGE CREDENTIALS
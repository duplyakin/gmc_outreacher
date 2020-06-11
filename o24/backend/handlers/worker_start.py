#!/usr/bin/env python
import os
from o24.backend import celery, create_app, app

#app = create_app()
app.app_context().push()

from o24.backend.handlers.jobs_map import *
from o24.backend.handlers.scheduler import *
from o24.backend.handlers.email import *
from o24.backend.handlers.enricher import *
from o24.backend.handlers.general import *

env = os.environ.get('APP_ENV', None)
if env == "Test":
    from .dummy import *


#celery -A o24.backend.handlers.worker_start.celery worker -E -l info -P gevent

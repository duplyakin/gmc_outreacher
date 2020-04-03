#!/usr/bin/env python
import os
from o24.backend import celery, create_app
from .jobs_map import *
from .dummy import *
from .scheduler import *

app = create_app()
app.app_context().push()

#celery -A o24.backend.handlers.worker_start.celery worker -E -l info -P gevent

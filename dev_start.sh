#!/bin/bash
set -e

./.venv/bin/gunicorn -c ./o24/gunicorn_config_dev.py -e APP_ENV=Test o24.wsgi:app

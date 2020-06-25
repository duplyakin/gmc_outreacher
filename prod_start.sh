#!/bin/bash
set -e

./.venv/bin/gunicorn -c ./o24/gunicorn_config_prod.py -e APP_ENV=Production o24.wsgi:app

#!/bin/bash
set -e

APP_ENV=Test python -m unittest discover -s ./o24/production_tests/ -p '*1_models.py'

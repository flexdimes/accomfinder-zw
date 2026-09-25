#!/usr/bin/env bash
# Runs automatically on every deploy to Render.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

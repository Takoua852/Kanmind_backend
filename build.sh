#!/bin/sh
set -e

python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
fullname = os.environ.get('DJANGO_SUPERUSER_FULLNAME', 'Admin User')

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        fullname=fullname,
        password=password
    )
    print("Superuser created")
else:
    print("Superuser already exists")
EOF
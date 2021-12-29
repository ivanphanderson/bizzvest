#!/bin/bash
python manage.py makemigrations 
python manage.py makemigrations models_app
python manage.py makemigrations faq
python manage.py makemigrations home_page
python manage.py makemigrations halaman_toko
python manage.py migrate
python manage.py migrate models_app
python manage.py migrate faq
python manage.py migrate home_page
python manage.py migrate halaman_toko
echo "deployment.sh success"
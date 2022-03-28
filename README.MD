# Tech stack: 

Django

Django rest_framework

MySQL

Big Qurey

Package Management: pipenv

# Commands

pip3 install pipenv -- install python package management tool

pipenv install django -- install django python framework and virtual environment

pipenv shell -- active shell in virtual environment

django-admin startproject PROJECT_NAME . -- create project under current folder

python manage.py runserver [PORT_NUMBER] -- run dev server

python manage.py startapp APP_NAME -- create a new app

# Select Virtual Environment Python Interpreter (Windows)

py -3 -m venv .venv

.venv\scripts\activate

View > Command Palette > Python: Select Interpreter

# Database Migaration

python manage.py makemigrations

python manage.py migrate
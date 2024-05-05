# Vendor-Management-System-with-Performance-Metrics
Vendor Management System with Performance Metrics
Install virtualenv:

with virtualenv create virutalenvironment v
#pip install virtualenv

Create a virtual environment named 'env'
#virtualenv env

On macOS/Linux:
source env/bin/activate

On Windows:
.\env\Scripts\activate

use this command to install required packages

pip install -r requirements.txt 

Install Django and Django REST Framework
pip install django djangorestframework

Create a Django project named 'vendor':
django-admin startproject vendor

Navigate to the project directory
cd vendor

Run the development server
python manage.py runserver

This sequence of commands will create a virtual environment, install Django and Django REST Framework within it, create a Django project named 'vendor', and start the development server. Make sure to activate the virtual environment before installing Django and running the server.


API to create user to login and create

Api to creat user:
POST :/api/user/

payload:
{
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password":"password"
}

example :auth token {
    "AuthToken": "3b31a4ba8255f24a48fa6bc7d808648f8ca4f720"
}



Api to Login user:
POST: /api/user/login/

payload:
{
    "email":"john@example.com"
}







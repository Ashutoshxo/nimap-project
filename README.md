🚀 Project Overview

This project is a Django REST API solution for managing:
- Users (Django's built-in auth)
- Clients
- Projects assigned to users

It fulfills all requirements from the machine test brief including:
- Client creation, update, delete
- Project creation under clients
- Assigning users to projects
- Retrieving projects assigned to the logged-in user


Set Up Virtual Environment

python -m venv envi
source envi/Scripts/activate

Install Dependencies
pip install -r requirements.txt

Create Superuser 
python manage.py createsuperuser

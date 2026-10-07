# Faculty Management System - Django MVT

## Features
- Faculty login
- Roles: Faculty, HOD, Dean, Director, Principal
- CL: 1 per calendar month
- Permission: 2 hours per calendar month; max 1 hour per request
- EL: 12 days per June-May leave year
- Medical Leave: 6 days per June-May leave year
- Leave approval
- Task assignment
- Circular publishing
- Birthday and joining-anniversary dashboard wishes
- Bootstrap responsive UI
- Django ORM and SQLite database

## 1. Create virtual environment
Windows:
    python -m venv .venv
    .venv\Scripts\activate

## 2. Install packages
    pip install -r requirements.txt

## 3. Create migrations
    python manage.py makemigrations
    python manage.py migrate

## 4. Create admin
    python manage.py createsuperuser

## 5. Create role groups
    python manage.py shell

Then run the commands from setup_roles.py, or execute:
    exec(open("setup_roles.py").read())

## 6. Start server
    python manage.py runserver

Open:
    http://127.0.0.1:8000/

Admin:
    http://127.0.0.1:8000/admin/

## Leave-year interpretation
"June to June" is implemented as a June 1 through May 31 leave year. If your institution means a different boundary, change leave_year_bounds() in leave_management/services.py.

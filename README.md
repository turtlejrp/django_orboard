# Django Project

## Project Overview

This is a Django project designed to collect Production Data and calculate Operation Ratio and 
also can report and analysis lost.

## Features

- Calculate Operations Ratio from Production and analysis details by hour and shift
- Report Loss in production for improvement
- Analysis Loss by type,shift,date

## Requirements

- Python 3.12
- Django 5.0.x
- SQLite (default) or any other database (PostgreSQL, MySQL, etc.)
- Other dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/turtlejrp/django_orboard.git
   cd ORBOARD
   ```

2.**Install Requirement Package**
   ```
   pip install -r requirements.txt
   ```

3.**Apply the database migrations:**
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

4.**Create a superuser:**
  ```
  python manage.py createsuperuser
  ```

5.**Collect static files:**
  ```
  python manage.py collectstatic
  ```

6.**Run the development server:**
  ```
  python manage.py runserver
  ```

## Application Usage
**

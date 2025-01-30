# Student Enrollment

## Requirements
- Python 3.13.0
- psql 17.2
- Django 5.1.5
- psycopg 3.2.4
- dgango-environ 0.12.0

## Instructions
1. In a terminal, navigate to your preferred directory and use the command:
>`git clone https://github.com/gerald-guerrero/student_enrollment.git`
2. CD into the repository:
>`cd student_enrollment`
3. Create a virtual environment:
>`python -m venv venv`
4. Activate the virtual environment:
>`venv\Scripts\activate`
5. Install all dependencies:
>`pip install -r requirements.txt`
6. CD into the project:
>`cd myproject`
7. create a .env file and fill out the following environmental variables\
with your postgresql database information
```bash
DB_NAME=your_db_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```
8. create db tables in your database:
>`python manage.py migrate`
9. create a superuser for the admin page
>`python manage.py createsuperuser`
8. Run the app with:
>`python manage.py runserver`
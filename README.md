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
7. create a .env file in the the current directory and fill out the following environmental variables\
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
10. Run the app with:
>`python manage.py runserver`

## Test Instructions
### students records
__Create__
1. In the nav bar, click the `New Students Enroll` link 
2. Fill out the form with the required information and submit

__Read__
1. Click the `Students` nav bar link to view a list of students
2. Click the `view` link next to the student you just created

__Update__
1. Go to the student details page of the student you created
2. Click the `Withdraw` button next to a section to withdraw\
from the associated section for the current student
3. Click the `Update Info` link to go to the update page
4. Change any of the student fields and click submit

__Delete__
1. On the student details page, click the `Delete` link
2. Confirm your deletion by clicking the `Delete` button

### section records
__Create__\
Sections can only be created in the admin page, as students and staff\
should not have create permissions for sections

__Read__
1. Click the `Sections` nav bar link to view a list of sections
2. Click the `view` link next to a section to view the associated\
section detail page

__Update__
1. The `Enroll Test` button will enroll a student into a section but\
will be fully implemented after account authentication is implemented
2. From the sections detail page, click the `Update` link to go to the\
section update page
3. Edit the list of enrolled students by updating the checkbox and\
click the submit button

__Delete__\
Sections can only be deleted in the admin page, as students and staff\
should not have delete permissions for sections
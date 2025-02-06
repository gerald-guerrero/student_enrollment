# Student Enrollment

## Requirements
- Python 3.13.0
- psql 17.2
- Django 5.1.5
- psycopg 3.2.4
- dgango-environ 0.12.0
- django-allauth 65.3.1
- django-allauth[socialaccount]

## Instructions
### Google API Setup for Allauth
1. Go to https://console.cloud.google.com/
2. In the sidebar, go to __APIs & Services__ then > __Credentials__ > __CREATE CREDENTIALS__ >__OAuth client ID__
3. Set application type to Web application and __Authorized redirect URIs to `http://127.0.0.1:8000/accounts/google/login/callback/`
4. Continue the application process (it make ask you to fill out an additonal process)
5. Save the __Client ID__ and __Client Secret__ (will be used later in the Django admin. Do not save in repository)

### Cloning Repository
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

### Database Setup
1. CD into the root myproject directory:
>`cd myproject`
2. create a .env file in the the current directory and fill out the following environmental variables\
with your postgresql database information
```bash
DB_NAME=your_db_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port
```
3. create db tables and allauth  in your database:
>`python manage.py migrate`
4. create a superuser for the admin page
>`python manage.py createsuperuser`

### Finalize Setup
1. While in the root directory, myproject:
>`python manage.py runserver`
2. Go http://127.0.0.1:8000/admin and sign in to the admin page with the superuser credentials
3. Go to __Social applications__
4. Click __ADD SOCIAL APPLICATION__
5. Fill out the form with the __Client ID__ and __Secret Key__ you received from the Google API setup
6. In the __Sites__ field, add localhost to __Chosen site__. You may need to create it with the green plus button
7. In the top right, click __logout__
8. Click the __login__ button the click __Sign Up__
9. Either go through sign up form or sign in with Google with the bottom link\

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
3. In the Enrolled Students table, click the `withdraw` button next to\
the student you wish to remove from the section
4. Select a student from the drop down menu and click `enroll` to enroll\
the student into the associated section

__Delete__\
Sections can only be deleted in the admin page, as students and staff\
should not have delete permissions for sections
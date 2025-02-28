# Student Enrollment

## Requirements
- Python 3.13.0
- psql 17.2
- aws-cli
- Docker 27.5.1
- Docker Desktop 4.38.0
- Django 5.1.5
- psycopg 3.2.4
- psycopg-binary 3.2.4
- psycopg-pool 3.2.4
- django-allauth 65.3.1
- django-allauth[socialaccount]
- djangorestframework 3.15.2
- django-filter 25.1

## Instructions

### AWS EC2 And ECR Setup
1. Login in to AWS and go to the IAM page
2. Create a role for an `AWS Service` entity and `EC2` use case with the  
`AmazonEC2ContainerRegistryReadOnly` permission
3. Go to the Elastic Container Registry page and create a repository
4. **Take note of the repository uri**
5. Go to the EC2 page, then go to the Instances tab, and Click Launch Instances
6. Configure the instance settings with:
    - Amazon Linux 2 AMI
    - t2.micro free tier
    - allow ssh traffic from your IP address
    - allow http traffic from the insternet
    - in Advanced Details, click the IAM instance profile option and select the IAM role you made
7. Launch the instance and create a new key pair
8. **Save the .pem key and take note of the public ipv4 address and the public ipv4 dns**

### Repository Setup
1. In a terminal, navigate to your preferred directory and use the command:
>`git clone https://github.com/gerald-guerrero/student_enrollment.git`
2. CD into the repository:
>`cd student_enrollment`
3. CD into the root project folder:
>`cd myproject`
4. Create a .env file in the the current directory and fill it out according to the .env.example  
This includes youer ipv4 address and ipv4 dns you noted earlier  
**For ALLOWED_HOSTS, ensure every host is separated by a single space and keep DEBUG=False**  
5. In the docker-compose.yml file, change the web: image: content from  
`123456789012.dkr.ecr.us-east-1.amazonaws.com/my-django-app:latest`  
to **use the repository uri you noted earlier and append :latest** so it matches the previous format
(the image will be built and pushed in the next section)

### AWS Deploment (Production)
1. Use the following commands to build and push image to your aws container registry  
(use your repository uri and region)  
- `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com`  
- `docker build -t my-django-app .`  
- `docker tag my-django-app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-django-app:latest`  
- `docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-django-app:latest`
2. Copy your .env and docker-compose.yml file to the ec2 with the command  
(use the path for the .pem key and the ec2 public ip address you noted earlier)  
- `scp -i /path/to/key.pem docker-compose.yml .env ec2-user@<EC2-Public-IP>:~`
3. Connect to the ec2  
(use the path for the .pem key and the ec2 public ip address you noted earlier)  
- `ssh -i /path/to/key.pem ec2-user@<EC2-Public-IP>`
4. Use the following commands to update the ec2 and install docker  
- `sudo yum update -y`  
- `sudo amazon-linux-extras install docker -y`  
- `sudo service docker start`  
- `sudo usermod -aG docker ec2-user`  
Logout and log back in to the instance  
- `DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)`  
- `sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-linux-$(uname -m)" -o /usr/local/bin/docker-compose`  
- `sudo chmod +x /usr/local/bin/docker-compose`  
5. Pull the django image and run the containers with  
- `docker-compose up -d`
6. if you run unto an `pull request denied` error, run the following commands to authenticate and run containers  
(use your repository uri and region)  
- `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com`  
- `docker-compose up -d`
7. While containers are running, create a superuser with  
- `docker-compose exec web python manage.py createsuperuser`

### Run Locally (Development)
1. Create a .env.dev file in the the current directory and fill it out according to the .env.dev.example  
**Keep the values given in the example for DEBUG and ALLOWED_HOSTS**  
2. Create and run the containers with docker-compose.dev.yml:  
- `docker-compose --file docker-compose.dev.yml up --build`
3. In a separate terminal create a superuser:  
- `docker-compose --file docker-compose.dev.yml exec web python manage.py createsuperuser`
4. Use ctrl+c to stop running the containers and the following command to start them again:  
- `docker-compose --file docker-compose.dev.yml up`
5. The containers will run on http://localhost:8000

### Google API Setup for Allauth
1. Go to https://console.cloud.google.com/
2. In the sidebar, go to __APIs & Services__ then > __Credentials__ > __CREATE CREDENTIALS__ >__OAuth client ID__
3. Set application type to Web application and add one or both of the following to __Authorized redirect URIs__  
(Replace with your ec2 ipv4 dns, for production)  
- `ec2-xx-xx-xxx-xxx.compute-1.amazonaws.com/accounts/google/login/callback/`  
(Add the following to access feature locally, for development)  
- `http://127.0.0.1:8000/accounts/google/login/callback/`
- `http://localhost:8000/accounts/google/login/callback/`
4. Continue the application process (it make ask you to fill out an additonal process)
5. Save the __Client ID__ and __Client Secret__ (will be used later in the Django admin. Do not save in repository)

### Admin Page Setup
1. Go to your ec2 ipv4 dns (or http://localhost:8000 if running locally) to view the homepage and click the Login link in the nav bar
2. Sign in with your superuser credentials, then click the Admin page link in the nav bar
3. Go to __Sites__ and click example.com if available. Replace domain name and display name with your  
ec2 ipv4 dns (or 'localhost' if running locally)  
4. If example.com is not there, click ADD SITE and use your ec2 ipv4 dns (or 'localhost' if running locally)
5. Go to __Social applications__
6. Click __ADD SOCIAL APPLICATION__
7. Fill out the form with the __Client ID__ and __Secret Key__ you received from the Google API setup
8. In the __Sites__ field, add the site you made or edited previously to __Chosen site__
9. Go to __Groups__ and click __ADD GROUP__
10. Name it "staff" and add the following permissions 
    - Myapp | course | can view course
    - Myapp | major | can view major
    - Myapp | professor | can view professor
    - Myapp | schedule | can view schedule
    - Myapp | section | can view section
    - Myapp | section enrollment | can change section enrollment
    - Myapp | section enrollment | can view section enrollment
    - Myapp | student | can change student
    - Myapp | student | can delete student
    - Myapp | student | can view student

### Account Creation
1. To create a staff user, go to __Users__ and click __ADD USER__ in the top right
2. Fill out the login credentials and create the user
3. For the newly created user, click __Staff status__ to make it active and in __Groups__ add the "staff" group, then save
4. To create a student user, click __logout__ in the top right
5. Click the __login__ button the click __Sign Up__
6. Either go through sign up form or sign in with Google with the bottom link

## Test Instructions
### students records
- __Create__
1. In the nav bar, click the `Login` link 
2. Click the `Sign Up` link in the top menu
3. Fill out the form to create a student user or click the Google login option to sign up with Google

- __Read__
1. For student users, click the `Profile` link in the nav bar
2. For staff users, click the `Students` link and click the `view` button of any student

- __Update__
1. On the `Student Details` page, click the `Update Info` button under `Student Options`
2. Change any of the student fields and click `Submit` to change the student's information
3. Student users will see an extra `Withdraw` button next to each enrolled section which can be\
clicked to remove that section from the student's sections

- __Delete__
1. On the student details page, click the `Delete` link
2. Confirm your deletion by clicking the `Delete` button

### section records
- __Create__
    - Sections can only be created in the admin page, as students and general staff\
    should not have create permissions for sections

- __Read__
1. Click the `Sections` nav bar link to view a list of sections
2. Click the `view` link next to a section to view the associated\
`Section Details` page
3. The `Student Details` page also has a view button next to the student's\
enrolled sections to view the associated `Section Details` page

- __Update__
1. On the `Section Details` page, if logged in as a student, the `Enroll` button\
will enroll a student into a section if checks are passed
2. On the `Section Details` page, if logged in as a staff user, click the `Update`\ 
button to go to update the section enrollments
3. To remove a student from a section, click the `Withdraw` button next to the student
4. To add a student, select a student from the drop down menu, and click the `Enroll` button

- __Delete__
    - Sections can only be deleted in the admin page, as students and general staff\
    should not have delete permissions for sections

## DRF API
### Endpoints
- Default Basic Root View (Requires Authentication):  
    - http://localhost:8000/api/  


- Public API Endpoints: 
    > Requires no authentication, read-only
    - http://localhost:8000/api/professors/
    - http://localhost:8000/api/professors/<id>
    - http://localhost:8000/api/majors/
    - http://localhost:8000/api/majors/<id>
    - http://localhost:8000/api/courses/
    - http://localhost:8000/api/courses/<id>
    
- All Authenticated API Endpoints:
    > Requires authentication, read-only
    - http://localhost:8000/api/sections/
    - http://localhost:8000/api/sections/<id>
    - http://localhost:8000/api/schedules/
    - http://localhost:8000/api/schedules/<id>

- Staff Only API Endpoints:
    > Requires staff user, read-only
    - http://localhost:8000/api/students/

- Staff or Student Object Owner Endpoints:
    - http://localhost:8000/api/students/<id>
        - read-only
    - http://localhost:8000/api/enrollments/
        - Only Staff can view entries
        - Staff can use Create operation for all students
        - Student users can use Create operation for themselves, not other student users
    - http://localhost:8000/api/enrollments/<id>
        - Staff can use Read, Update, Delete
        - Student users can use Read, Update, Delete for their own entries

### Filtering, Searching, And Pagination
to add search, filter, or page fields to the api endpoint, follow the format:  
`http://localhost:8000/api/<viewset>/?<FilterField=Value>&<search=Value>&<page=value>`  
Multiple filter fields may be included depending on the viewset  
The 'search' field can be used to search some fields with partial information
The 'page' field can be used to navigate multiple pages if results exceed the page limit size

- students
    - filter fields
        - `major`: id
        - `semester_enrolled`: string option
        - `year_enrolled`: int
    - search fields
        - first and last name
- professors
    - filter fields
        - `department`: string option
    - search fields
        - first and last name
- majors
    - search fields
        - major title
- courses
    - filter fields
        - `major`: id
        - `name`: string
        - `credits: int`
    - search fields
        - course name
- sections
    - filter fields
        - `course`: id
        - `professor`: id
        - `building`: string
        - `room`: string
        - `semester`: string option
        - `year`: int
    - search fields
        - course name
- schedules
    - filter fields
        - `section`: id
        - `class_day`: string option
        - `start_time`: time 
        - `end_time`: time
    - search fields
        - section's course name
- enrollments
    - filter fields
        - `section`: id
        - `student`: id
    - search fields
        - section's course name
        - student first and last name
from django.db import models

class Semesters(models.TextChoices):
    """
    Semester options are based on University course cycle
    options are used for student enrollment and section attributes
    """
    FALL = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"

class Major(models.Model):
    """
    Stores all available majors for the enrollment system.
    Can be updated with more entries if needed
    is used for every student and course with a one to many relationship
    """
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

class Student(models.Model):
    """
    Contains all relevant information for students including name, major, as well as the semester
    and year they enrolled for
    Has a many to many relation with section
    """
    major = models.ForeignKey(Major, related_name="students", related_query_name="student", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    semester_enrolled = models.CharField(max_length=10, choices=Semesters.choices, help_text="Select the semester the student will begin classes")
    year_enrolled = models.IntegerField(help_text="Provide the year the student will begin classes")
    
    def __str__(self):
        return f"{self.id}. {self.first_name } {self.last_name}"

class Professor(models.Model):
    """
    Stores name and department (using DEPARTMENT choice option) for every professor in the system
    has a one to many relationship with section
    """
    DEPARTMENT = {
        "Business": "Business",
        "Mathematics": "Mathematics",
        "Engineering": "Engineering"
    }
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50, choices=DEPARTMENT)
    
    def __str__(self):
        return f"{self.first_name } {self.last_name}"

class Course(models.Model):
    """
    Stores basic information of the name, major, and credits of every course offered
    has a one to many relationship with section
    """
    name = models.CharField(max_length=50)
    major = models.ForeignKey(Major, related_name="courses", related_query_name="course", on_delete=models.CASCADE)
    credits = models.IntegerField(help_text="Provide the number of credits the course is worth")

    def __str__(self):
        return self.name

class Section(models.Model):
    """
    Stores the relevant information for every section (class) available for registration
    This includes the location, semester, and year the section is offered
    Also has related information with the course and professor using foreign keys to link them
    Uses ManyToManyField to link all students registered to this section
    has a one to many relationship with schedule
    """
    course = models.ForeignKey(Course, related_name="sections", related_query_name="section", on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, related_name="sections", related_query_name="section", on_delete = models.CASCADE)
    building = models.CharField(max_length=30, null=True, help_text="Provide the name of the building")
    room = models.CharField(max_length=10, null=True, help_text="Provide the room number")
    semester = models.CharField(max_length=10, choices=Semesters.choices, help_text="Select which semester the section will take place")
    year = models.IntegerField(help_text="Provide the year the section will take place")
    students = models.ManyToManyField(Student, related_name="sections", related_query_name="section")

    def __str__(self):
        return f"{self.id}. {self.building}-{self.room}, {self.semester} {self.year}"

class Schedule(models.Model):
    """
    Stores the schedule for every section which is liked by foreign key to the associated section
    uses choice option to select the meeting day
    """
    DAYS = {
        "Monday": "Monday",
        "Tuesday": "Tuesday",
        "Wednesday": "Wednesday",
        "Thursday": "Thursday",
        "Friday": "Friday",
    }
    section = models.ForeignKey(Section, related_name="schedules", related_query_name="schedule", on_delete=models.CASCADE)
    class_day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_day}: {self.start_time} - {self.end_time}"

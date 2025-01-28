from django.db import models

class Semesters(models.TextChoices):
    FALL = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"

class Major(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

class Student(models.Model):
    major = models.ForeignKey(Major, related_name="students", related_query_name="student", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    semester_enrolled = models.CharField(max_length=10, choices=Semesters.choices)
    year_enrolled = models.IntegerField()
    
    def __str__(self):
        return f"{self.id}. {self.first_name } {self.last_name}"

class Professor(models.Model):
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
    name = models.CharField(max_length=50)
    credits = models.IntegerField()

    def __str__(self):
        return self.name

class Section(models.Model):

    course = models.ForeignKey(Course, related_name="sections", related_query_name="section", on_delete=models.CASCADE)
    major = models.ForeignKey(Major, related_name="sections", related_query_name="section", on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, related_name="sections", related_query_name="section", on_delete = models.CASCADE)
    building = models.CharField(max_length=30, null=True)
    room = models.CharField(max_length=10, null=True)
    semester = models.CharField(max_length=10, choices=Semesters.choices)
    year = models.IntegerField()
    students = models.ManyToManyField(Student, related_name="sections", related_query_name="section")

    def __str__(self):
        return f"{self.id}. {self.building}-{self.room}, {self.semester} {self.year}"

class Schedule(models.Model):
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

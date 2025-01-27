from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    enrollment_date = models.DateField()
    
    def __str__(self):
        return f"{self.id}. {self.first_name } {self.last_name}"

class Professor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.first_name } {self.last_name}"

class Course(models.Model):
    name = models.CharField(max_length=50)
    credits = models.IntegerField()

    def __str__(self):
        return self.name

class Section(models.Model):
    SEMESTERS = {
        "fall": "Fall",
        "spring": "Spring",
        "summer": "Summer",
    }
    course = models.ForeignKey(Course, related_name="sections", related_query_name="section", on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, related_name="sections", related_query_name="section", on_delete = models.CASCADE)
    building = models.CharField(max_length=30, null=True)
    room = models.CharField(max_length=10, null=True)
    semester = models.CharField(max_length=10, choices=SEMESTERS)
    year = models.IntegerField()
    students = models.ManyToManyField(Student, related_name="sections", related_query_name="section")

    def __str__(self):
        return f"{self.id}. {self.building} room {self.room}, {self.semester} {self.year}"

class Schedule(models.Model):
    DAYS = {
        "monday": "Monday",
        "tuesday": "Tuesday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
    }
    section = models.ForeignKey(Section, related_name="schedules", related_query_name="schedule", on_delete=models.CASCADE)
    class_day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_day}: {self.start_time} - {self.end_time}"

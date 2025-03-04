from django.db import models
from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse
from django.contrib.auth.models import User

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
    Has a one to one relationship with Django User
    Contains all relevant information for students including name, major, as well as the semester
    and year they enrolled for
    Has a many to many relation with section
    """
    YEAR_CHOICES = [(year, year) for year in range(2024, 2100)]
    
    user = models.OneToOneField(User, related_name="student", related_query_name="student", on_delete=models.CASCADE)
    major = models.ForeignKey(Major, related_name="students", related_query_name="student", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    semester_enrolled = models.CharField(max_length=10, choices=Semesters.choices, help_text="Select the semester the student will begin classes")
    year_enrolled = models.IntegerField(choices=YEAR_CHOICES, help_text="Select the year the student will begin classes")
    
    def __str__(self):
        return f"({self.id}) {self.first_name } {self.last_name}"
    
    def clean(self):
        check_year(self.year_enrolled)

    def get_all_schedules(self):
        sections = self.sections.all()
        section_schedules = [section.schedules.all() for section in sections]
        schedules = [schedule for section in section_schedules for schedule in section]
        return schedules
    
    def get_absolute_url(self):
        return reverse("student_detail", kwargs={"pk": self.pk})
    
    

class Professor(models.Model):
    """
    Stores name and department (using DEPARTMENT choice option) for every professor in the system
    has a one to many relationship with section
    """
    DEPARTMENT = {
        "Humanities": "Humanities",
        "Communication & Media Studies": "Communication & Media Studies",
        "Law": "Law",
        "Social Sciences": "Social Sciences",
        "Business & Management": "Business & Management",
        "Education": "Education",
        "Health & Medical Sciences": "Health & Medical Sciences",
        "Biological & Life Sciences": "Biological & Life Sciences",
        "Physical Sciences": "Physical Sciences",
        "Mathematics & Statistics": "Mathematics & Statistics",
        "Computer Science & Information Technology": "Computer Science & Information Technology",
        "Engineering": "Engineering"
    }
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50, choices=DEPARTMENT)
    
    def __str__(self):
        return f"{self.first_name } {self.last_name} - {self.department}"

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
    size = models.IntegerField(default=50, help_text="Provide the maximum amount of students that can register for this section")
    students = models.ManyToManyField(Student, related_name="sections", related_query_name="section", through="Enrollment", blank=True)

    def __str__(self):
        return f"({self.id}) {self.course.name}, {self.semester} {self.year}"
    
    def clean(self):
        check_year(self.year)

    def is_full(self):
        if self.students.all().count() >= self.size:
            return True
        
    def get_schedules(self):
        return self.schedules.all()
    
    def get_capacity_str(self):
        return f"{self.students.all().count()} / {self.size}"
    
    def get_schedules_str(self):
        full_schedule = [str(schedule) for schedule in self.schedules.all()]
        return "\n".join(full_schedule)
    
    def get_absolute_url(self):
        return reverse("section_update", kwargs={"pk": self.pk})

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
    
    def clean(self):
        if is_time_conflict([self], self.section.schedules.exclude(pk=self.pk).all()):
            raise ValidationError("Time Slots Overlap")
        
class Enrollment(models.Model):
    """
    Many to Many model designated in the 'through' field for Section students attribute
    """
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=['section', 'student'], name='unique_enrollment')]
    
    def __str__(self):
        major = self.section.course.major
        course = self.section.course
        section = self.section.id
        student = self.student
        return f"{major}, {course} [{section}], {student}"
    
    def clean(self):
        section = self.section
        student = self.student

        if section.is_full():
            raise ValidationError("Section is full")
        
        if is_time_conflict(student.get_all_schedules(), section.get_schedules()):
            raise ValidationError("Time conflict")

def check_year(year):
    year_min = 2024
    year_max = 2100
    if not (year_min <= year <= year_max):
        raise ValidationError(f"Year selections must be between {year_min} - {year_max}")

def is_time_conflict(original_schedules, requested_schedules):
    # compares schedules to check if any time slots overlap with each other
    for original_slot in original_schedules:
        for requested_slot in requested_schedules:
            if (original_slot.start_time <= requested_slot.end_time and 
                original_slot.end_time >= requested_slot.start_time and
                original_slot.class_day == requested_slot.class_day):
                return True
    return False

@receiver(post_delete, sender=Student)
def delete_student_user(sender, instance, **kwargs):
    instance.user.delete()

@receiver(m2m_changed, sender=Section.students.through)
def enrollment_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if (action !="pre_add"):
        print("not checking", action)
        return

    schedules = Schedule.objects

    if reverse:
        requested_sections = Section.objects.filter(pk__in=pk_set).all()

        student_schedules = instance.get_all_schedules()
        requested_schedules = schedules.filter(section__in=requested_sections).all()

        if is_time_conflict(student_schedules, requested_schedules):
            # prevents all student enrollments for sections if there is a time conflict
            print("Time conflict. No sections will be enrolled")
            pk_set.clear()
        
        for pk in pk_set.copy():
            section = Section.objects.get(pk = pk)
            if section.is_full():
                # prevents student enrollment for only full sections
                print("Section is full. This section will not be enrolled")
                pk_set.remove(pk)
        
    else:
        for pk in pk_set.copy():
            student_sections = model.objects.get(pk=pk).sections.all()
            
            student_schedules = schedules.filter(section__in=student_sections).all()
            requested_schedules = schedules.filter(section=instance).all()
            if is_time_conflict(student_schedules, requested_schedules):
                # prevents section enrollments for only students that have a time conflict
                print("time conflict: Student will not be enrolled")
                pk_set.remove(pk)

        limit = instance.size
        future_total_students = instance.students.all().count() + len(pk_set)
        if future_total_students > limit:
            # prevents all section enrollments if it would push section above the size limit
            print("Section is full. No student will be enrolled")
            pk_set.clear()

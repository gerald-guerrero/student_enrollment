from django.shortcuts import render
from .models import Student, Professor, Course, Section, Schedule

# Create your views here.
def course_data(request):
    sections = Section.objects.select_related('course', 'professor')
    sections_info = []
    for section in sections:
        course_section = f"{section.course.course_name} - Section {section.id}\n"
        location = f"Location: {section.building} - room {section.room}\n"
        professor = f"Professor: {section.professor.first_name} {section.professor.last_name}\n"
        schedules = f"Section Schedule"
        for schedule in section.schedules.all():
            schedules += f"\n  {schedule.class_day}: {schedule.start_time} - {schedule.end_time}"
        students = f"\nStudents Registered"
        for student in section.students.all():
            students += f"\n  {student.id}. {student.first_name} {student.last_name}"
        sections_info.append(course_section + location + professor + schedules + students + "\n")

    return render(request, "index.html", {"sections_info": sections_info})
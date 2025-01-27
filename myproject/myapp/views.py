from django.shortcuts import render
from .models import Section

# Create your views here.
def course_data(request):
    sections = Section.objects.select_related('course', 'professor').prefetch_related('students')
    sections_info = []
    for section in sections:
        course_section = f"{section.course.__str__()} - Section {section.id}\n"
        details = f"Details: {section.__str__()}\n"
        professor = f"Professor: {section.professor.__str__()}\n"
        schedules = f"Section Schedule"
        for schedule in section.schedules.all():
            schedules += f"\n  {schedule.__str__()}"
        students = f"\nStudents Registered"
        for student in section.students.all():
            students += f"\n  {student.__str__()}"
        sections_info.append(course_section + details + professor + schedules + students + "\n")

    return render(request, "index.html", {"sections_info": sections_info})
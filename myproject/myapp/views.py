from django.shortcuts import render
from .models import Section

# Create your views here.
def course_data(request):
    """
    Obtains every section (class) available and joins it with the relevant course, professor, and
    students tables, then sorts the sections by their course major.
    The loop iterates through every section and compiles the relevant data into a list of dicts.
    Renders index.html template with the compiled section information as context
    """
    sections = (Section.objects.select_related('course', 'professor')
                     .prefetch_related('students').all().order_by('course__major__title'))
    sections_info = []
    for section in sections:
        details = {
            "major": section.course.major,
            "name": section.course.name,
            "section_id": section.id,
            "credits": section.course.credits,
            "semester": section.semester,
            "year": section.year,
            "professor": section.professor,
            "schedule": "\n".join([schedule.__str__() for schedule in section.schedules.all()]),
            "students": "\n".join([student.__str__() for student in section.students.all()])
        }
        sections_info.append(details)

    return render(request, "index.html", {"sections_info": sections_info})
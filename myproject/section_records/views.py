from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from myapp.models import Section, Student, is_time_conflict
from django.views.generic import ListView, DetailView
from .forms import SectionStudentForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from myapp.user_status import user_is_student, user_is_staff

class SectionListView(ListView):
    """
    Generic list view for the Section model
    """

    model = Section
    template_name = 'section_records/section_list.html'

class SectionDetailView(DetailView):
    """
    Generic Detail view for the Section model entry
    """

    model = Section
    template_name = 'section_records/section_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        section = context['section']

        if (not user.is_staff):
            if (not section in user.student.sections.all()):
                context["is_enrolled"] = True
        else:
            context["is_enrolled"] = False
        
        return context
    
@user_passes_test(user_is_staff)
def section_update(request, pk):
    """
    Handles staff authorised enrollments and withdrawls for the associated section
    checks whether enroll or withdraw button was selected before proceeding
    enroll feature uses custom model form to get the requested student and enroll
    withdraw feature uses standard html form as it is just a button and a hidden student pk value
    """
    section = get_object_or_404(Section, pk=pk)
    students = section.students.all().order_by('id')
    
    form = SectionStudentForm(instance=section)
    if (request.method == 'POST') and ("enroll" in request.POST):
        form = SectionStudentForm(request.POST, instance=section)
        if form.is_valid():
            student = form.cleaned_data['students']
            print(f"enrolling {student} into section: {section}")
            section.students.add(student)
            form = SectionStudentForm(instance=section)
    elif (request.method == 'POST') and ("withdraw" in request.POST):
        stu_pk = int(request.POST.get('stu_pk'))
        student = get_object_or_404(Student, pk=stu_pk)
        print(student, "withdrawing", section)
        section.students.remove(student)

    return render(request, "section_records/section_update.html", {"section": section, "students": students, "form": form})

@user_passes_test(user_is_student)
def enroll_section(request, pk):
    """
    Handles a student enrolling into a section by getting the referenced section
    Will fully implement after authentication is implemented
    """
    student = request.user.student
    section = get_object_or_404(Section, pk=pk)
    
    if section.is_full():
        messages.error(request, "Section is full. Section will not be added to your enrollments")
        return redirect('section_detail', pk=pk)
    elif is_time_conflict(student.get_all_schedules(), section.get_schedules()):
        messages.error(request, "Time Conflict. Section will not be added to your enrollments")
        return redirect('section_detail', pk=pk)
        
    if request.method == "POST":
        print("Attempting to enroll student", student, "to section:", section)
        print("Will redirect to same section page afterwards")
        student.sections.add(section)
    return redirect('section_detail', pk=pk)
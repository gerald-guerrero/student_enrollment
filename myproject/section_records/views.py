from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from myapp.models import Section, Student
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from .forms import SectionStudentForm
from django.contrib import messages
from django.core.exceptions import ValidationError

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

def section_update(request, pk):
    """
    Handles staff authorised enrollments and withdrawls for the associated section
    checks whether enroll or withdraw button was selected before proceeding
    enroll feature uses custom model form to get the requested student and enroll
    withdraw feature uses standard html form as it is just a button and a hidden student pk value
    """
    section = get_object_or_404(Section, pk=pk)
    form = SectionStudentForm()

    if (request.method == 'POST') and ("enroll" in request.POST):
        form = SectionStudentForm(request.POST, instance=section)
        if form.is_valid():
            student = form.cleaned_data['students']
            print(f"enrolling {student} into section: {section}")
            section.students.add(student)
    elif (request.method == 'POST') and ("withdraw" in request.POST):
        stu_pk = int(request.POST.get('stu_pk'))
        student = get_object_or_404(Student, pk=stu_pk)
        print(student, "withdrawing", section)
        section.students.remove(student)

    return render(request, "section_records/section_update.html", {"section": section, "form": form})

def enroll_section(request, pk):
    """
    Handles a student enrolling into a section by getting the referenced section
    Will fully implement after authentication is implemented
    """
    section = get_object_or_404(Section, pk=pk)
    if section.is_full():
        print("Section is full")
        messages.error(request, "Section is full. Section will not be added to your enrollments")
        
    if request.method == "POST":
        print("Attempting to enroll student to section: ", section)
        print("Will redirect to same section page afterwards")
    return redirect('section_detail', pk=pk)
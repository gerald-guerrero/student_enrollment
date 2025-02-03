from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from myapp.models import Section
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .forms import SectionStudentForm

class SectionListView(ListView):
    """
    Generic list view for the Section model
    """

    model = Section
    template_name = 'section_records/section_list.html'

class SectionUpdateView(UpdateView):
    """
    Generic update view for a single Section entry
    Uses a custom form to handle all student enrollments and custom sort the checkbox fields
    """
    model = Section
    template_name = 'section_records/section_enrollment.html'
    form_class = SectionStudentForm

def enroll_section(request, pk):
    """
    Handles enrolling a student into a section by getting the referenced section
    Will fully implement after authentication is implemented
    """
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        print("Attempting to enroll student to section: ", section)
        print("Will redirect to same section page afterwards")
    return redirect('section_update', pk=pk)
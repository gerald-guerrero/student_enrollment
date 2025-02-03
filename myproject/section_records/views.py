from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from myapp.models import Section
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from .forms import SectionStudentForm
from django.contrib import messages

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

class SectionUpdateView(UpdateView):
    """
    Generic update view for a single Section entry
    Uses a custom form to handle all student enrollments and custom sort the checkbox fields
    """
    model = Section
    template_name = 'section_records/section_update.html'
    form_class = SectionStudentForm

def enroll_section(request, pk):
    """
    Handles enrolling a student into a section by getting the referenced section
    Will fully implement after authentication is implemented
    """
    section = get_object_or_404(Section, pk=pk)
    if section.students.all().count() >= section.size:
        print("Section is full")
        messages.error(request, "Section is full. Section will not be added to your enrollments")
        
    if request.method == "POST":
        print("Attempting to enroll student to section: ", section)
        print("Will redirect to same section page afterwards")
    return redirect('section_detail', pk=pk)
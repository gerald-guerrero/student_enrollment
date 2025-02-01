from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from myapp.models import Section
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .forms import SectionStudentForm

class SectionListView(ListView):
    model = Section
    template_name = 'section_records/section_list.html'

class SectionUpdateView(UpdateView):
    model = Section
    template_name = 'section_records/section_enrollment.html'
    form_class = SectionStudentForm

def enroll_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        print("Attempting to enroll student to section: ", section)
        print("Will redirect to same section page afterwards")
    return redirect('section_update', pk=pk)

def withdraw_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        print("Attempting to withdraw student from section: ", section)
        print("Will redirect to same section page afterwards")
    return redirect('section_update', pk=pk)
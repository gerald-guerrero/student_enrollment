from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from myapp.models import Student

# Create your views here.
class StudentListView(ListView):
    model = Student
    template_name = 'student_records/student_list.html'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_records/student_detail.html'

class StudentCreateView(CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled']
    template_name = 'student_records/student_form.html'

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'major']
    template_name = 'student_records/student_form.html'
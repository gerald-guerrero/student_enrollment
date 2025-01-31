from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from myapp.models import Student

# Create your views here.
class StudentListView(ListView):
    model = Student
    template_name = 'student_records/student_list.html'

class StudentDetailView(DeleteView):
    model = Student
    template_name = 'student_records/student_detail.html'
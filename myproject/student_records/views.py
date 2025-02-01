from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from myapp.models import Student
from django.urls import reverse_lazy

# Create your views here.
class StudentListView(ListView):
    '''
    Generic CBV for list all created student objects
    '''
    model = Student
    template_name = 'student_records/student_list.html'

class StudentDetailView(DetailView):
    '''
    CBV that provides details on a specific student object
    '''
    model = Student
    template_name = 'student_records/student_detail.html'

class StudentCreateView(CreateView):
    '''
    Handles the creation of new students by auto generating a form based on the student model
    '''
    model = Student
    fields = ['first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled']
    template_name = 'student_records/student_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register Student"
        
        return context

class StudentUpdateView(UpdateView):
    '''
    Handles updating field of a specific student object except for the semester and year fields
    as those should not be updated
    '''
    model = Student
    fields = ['first_name', 'last_name', 'major']
    template_name = 'student_records/student_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Student"
        
        return context

class StudentDeleteView(DeleteView):
    '''
    Handles deletion of a given student object and redirects to the student list view if the 
    deletion goes through
    '''
    model = Student
    template_name = 'student_records/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
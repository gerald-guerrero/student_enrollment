from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from myapp.models import Student, Section
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from myapp.user_status import user_is_student, is_owner_or_staff

# Create your views here.
class StudentListView(UserPassesTestMixin, ListView):
    '''
    Generic CBV for list all created student objects
    '''
    model = Student
    template_name = 'student_records/student_list.html'
    ordering = 'id'

    def test_func(self):
        return self.request.user.is_staff

class StudentDetailView(UserPassesTestMixin, DetailView):
    '''
    CBV that provides details on a specific student object
    '''
    model = Student
    template_name = 'student_records/student_detail.html'

    def test_func(self):
        return is_owner_or_staff(self)

class StudentUpdateView(UserPassesTestMixin, UpdateView):
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
    
    def test_func(self):
        return is_owner_or_staff(self)

class StudentDeleteView(UserPassesTestMixin, DeleteView):
    '''
    Handles deletion of a given student object and redirects to the student list view if the 
    deletion goes through
    '''
    model = Student
    template_name = 'student_records/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def test_func(self):
        return is_owner_or_staff(self)

@user_passes_test(user_is_student)
def withdraw_section(request, student_pk, section_pk):
    """
    Withdraws student from section by removing student-section entry from many-to-many relationship
    Redirects to the student detail page
    """
    if not is_owner_or_staff(request, student_pk):
        raise PermissionDenied
    
    student = request.user.student
    section = get_object_or_404(Section, pk=section_pk)

    if request.method == "POST":
        print(f"{student} withdrawing from section: {section}")
        student.sections.remove(section)
    
    return redirect('student_detail', pk=student_pk)


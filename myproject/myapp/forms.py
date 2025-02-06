from allauth.account.forms import SignupForm
from django import forms
from .models import Student
from django.core.exceptions import ValidationError

class StudentDetailsForm(forms.ModelForm):
    """
    Generic model form based on the Student model
    only used to auto create fields based on model
    fields
    """
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled']
    
    def clean(self):
        cleaned_data = super().clean()
        if self.fields['first_name'] == "gerald":
            raise ValidationError("test")
        
        return cleaned_data

class StudentSignupForm(SignupForm):
    """
    Sign up form is extended from allauth signup form to also create a Student profile
    that will be linked to the user.
    fields are taken from the StudentDetailsForm model form, so that the fields are auto
    generated to match the Student model
    """
    student_fields = StudentDetailsForm.base_fields
    first_name = student_fields['first_name']
    last_name = student_fields['last_name']
    major = student_fields['major']
    semester_enrolled = student_fields['semester_enrolled']
    year_enrolled = student_fields['year_enrolled']

    def save(self, request):
        user = super(StudentSignupForm, self).save(request)

        cleaned_data = self.cleaned_data

        Student.objects.create(
            user=user,
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            major=cleaned_data['major'],
            semester_enrolled=cleaned_data['semester_enrolled'],
            year_enrolled=cleaned_data['year_enrolled']
        )

        return user


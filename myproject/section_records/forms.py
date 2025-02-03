from django import forms
from myapp.models import Section, Student, is_time_conflict
from django.core.exceptions import ValidationError

class SectionStudentForm(forms.ModelForm):
    students = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('id')
    )

    class Meta:
        model = Student
        fields = ['students']

    def clean(self):
        cleaned_data = super().clean()
        section = self.instance
        student = cleaned_data.get('students')

        if section.is_full():
            raise ValidationError("Section is full. Enrollment will not occur")

        if is_time_conflict(student.get_all_schedules(), section.get_schedules()):
            raise ValidationError("Time conflict for selected student. Enrollment will not occur")

        return cleaned_data
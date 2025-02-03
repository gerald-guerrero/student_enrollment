from django import forms
from myapp.models import Section, Student, is_time_conflict
from django.core.exceptions import ValidationError

class SectionStudentForm(forms.ModelForm):
    """
    Model form that provides a model choice field of Students. Requires paramater, instance=section
    overrides __init__() to get the section and students enrolled in the section. Filters out 
    students that are already enrolled
    overrides clean() to add form validation. Raises validation error if section is full or section
    has a time conflict with the selected student's schedules
    """
    students = forms.ModelChoiceField(
        queryset=Student.objects.all().order_by('id')
    )

    class Meta:
        model = Student
        fields = ['students']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        section = self.instance
        enrolled_students = section.students.all()
        if enrolled_students:
            unenrolled_students = Student.objects.all().exclude(pk__in=enrolled_students).order_by('pk')
        else:
            unenrolled_students = Student.objects.all().order_by('pk')
        
        self.fields['students'].queryset = unenrolled_students

    def clean(self):
        cleaned_data = super().clean()
        section = self.instance
        student = cleaned_data.get('students')
        if section.is_full():
            raise ValidationError("Section is full. Enrollment will not occur")

        if is_time_conflict(student.get_all_schedules(), section.get_schedules()):
            raise ValidationError("Time conflict for selected student. Enrollment will not occur")

        return cleaned_data
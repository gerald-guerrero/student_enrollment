from django import forms
from myapp.models import Section, Student
from django.db.models import Value
from django.db.models import Case, When
from django.core.exceptions import ValidationError

class SectionStudentForm(forms.ModelForm):
    """
    Custom form to manage all student enrollments for this section
    Provides a checkbox of all students with the enrolled students pre-checked
    overrides __init__ to sort the checkbox fields with annotations by whether 
    they are enrolled or not
    """
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Section
        fields = ['students']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        enrolled_students = self.instance.students.all().annotate(enrolled=Value(1))

        all_students = Student.objects.all().annotate(
            enrolled=Case(
                When (pk__in=enrolled_students, then=Value(1)),
                default=Value(2),
            )
        )
        self.fields['students'].queryset = all_students.order_by('enrolled', 'id')

    def clean(self):
        cleaned_data = super().clean()
        section_size = self.instance.size
        selected_students_count = cleaned_data.get('students').count()

        if selected_students_count > section_size:
            raise ValidationError("Current student selections push section above its capacity.\
                                  Remove students and resubmit")
    
        return cleaned_data
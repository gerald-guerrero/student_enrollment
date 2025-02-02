from django import forms
from myapp.models import Student, Section

class EnrollmentForm(forms.ModelForm):
    sections = forms.ModelMultipleChoiceField(
        queryset=Section.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Student
        fields = ['sections']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        enrolled_sections = self.instance.sections.all()
        self.fields['sections'].queryset = enrolled_sections
        self.fields['sections'].initial = enrolled_sections
    
    def save(self):
        student = super().save(commit=False) 
        
        student.sections.set(self.cleaned_data['sections']) 

        student.save()
        self.save_m2m() 

        return student
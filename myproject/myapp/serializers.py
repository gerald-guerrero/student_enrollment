from rest_framework import serializers
from .models import Student, Professor, Major, Course, Section, Schedule

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled']
        
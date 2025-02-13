from rest_framework import serializers
from .models import Student, Professor, Major, Course, Section, Schedule

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled']
        
class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['first_name', 'last_name', 'department']

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    major = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField()
    class Meta:
        model = Schedule
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    professor = serializers.StringRelatedField()
    schedules = ScheduleSerializer(many=True, read_only=True)
    class Meta:
        model = Section
        fields = ['id', 'course', 'professor', 'building', 'room', 'semester', 'year', 'size', 'schedules']
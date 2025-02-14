from rest_framework import serializers
from .models import (Student, Professor, Major, Course, Section, Schedule, Enrollment,
                      is_time_conflict)
from django.core.exceptions import ValidationError

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

class EnrollmentSerializer(serializers.ModelSerializer):
    section_major = serializers.StringRelatedField(source="section.course.major")
    section_name = serializers.StringRelatedField(source="section")
    student_name = serializers.StringRelatedField(source='student')
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, attrs):
        user = self.context.get("request").user

        section = attrs['section']
        student = attrs['student']

        if (not user.is_staff): 
            if user.student != student:
                raise ValidationError("You cannot enroll another student")

        if section.is_full():
            raise ValidationError("Section is full")
        
        if is_time_conflict(student.get_all_schedules(), section.get_schedules()):
            raise ValidationError("Time conflict")
        return attrs
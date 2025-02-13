from django.shortcuts import render
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from .models import Student, Professor, Major, Course, Section, Schedule
from .serializers import (StudentSerializer, ProfessorSerializer, MajorSerializer,
                          CourseSerializer, SectionSerializer, ScheduleSerializer
                          )
from .permissions import StudentAccessPermission

@login_not_required
def homepage(request):
    """
    Basic homepage FBV. Renders index.html template with all features
    accessible from base.html nav bar
    """

    return render(request, "myapp/index.html")

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [StudentAccessPermission]
    http_method_names = ['get', 'head']

@method_decorator(login_not_required, name="dispatch")
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('id')
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']

@method_decorator(login_not_required, name="dispatch")
class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all().order_by('id')
    serializer_class = MajorSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']

@method_decorator(login_not_required, name="dispatch")
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by('id')
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('id')
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']
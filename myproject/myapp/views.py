from django.shortcuts import render
from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, routers
from .models import Student, Professor, Major, Course, Section, Schedule, Enrollment
from .serializers import (StudentSerializer, ProfessorSerializer, MajorSerializer,
                          CourseSerializer, SectionSerializer, ScheduleSerializer,
                          EnrollmentSerializer
                          )
from .permissions import StaffListOnly, IsStaffOrOwner
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

@login_not_required
def homepage(request):
    """
    Basic homepage FBV. Renders index.html template with all features
    accessible from base.html nav bar
    """

    return render(request, "myapp/index.html")

@method_decorator(login_not_required, name="dispatch")
class ApiRootView(routers.APIRootView):
    pass

@method_decorator(login_not_required, name="dispatch")
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [StaffListOnly, IsStaffOrOwner]
    http_method_names = ['get', 'head']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['major', 'semester_enrolled', 'year_enrolled']
    search_fields = ['first_name', 'last_name']

@method_decorator(login_not_required, name="dispatch")
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('id')
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department']
    search_fields = ['first_name', 'last_name']

@method_decorator(login_not_required, name="dispatch")
class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all().order_by('id')
    serializer_class = MajorSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title']

@method_decorator(login_not_required, name="dispatch")
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'head']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['major', 'name', 'credits']
    search_fields = ['name']

@method_decorator(login_not_required, name="dispatch")
class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by('id')
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'professor', 'building', 'room', 'semester', 'year']
    search_fields = ['course']

@method_decorator(login_not_required, name="dispatch")
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('id')
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['section', 'class_day', 'start_time', 'end_time']
    search_fields = ['section']

@method_decorator(login_not_required, name="dispatch")
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [StaffListOnly, IsStaffOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['section', 'student']
    search_fields = ['section', 'student']
    
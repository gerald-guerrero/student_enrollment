"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views
from rest_framework.routers import DefaultRouter
from myapp.views import (StudentViewSet, ProfessorViewSet, MajorViewSet,
                         CourseViewSet, SectionViewSet, ScheduleViewSet
                         )

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'professors', ProfessorViewSet, basename='professor')
router.register(r'majors', MajorViewSet, basename='major')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('students/', include('student_records.urls')),
    path('sections/', include('section_records.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include(router.urls)),
]

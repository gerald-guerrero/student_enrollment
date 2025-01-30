from django.contrib import admin
from .models import Major, Student, Professor, Course, Section, Schedule

# Register your models here.
@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled')
    search_fields = ('first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department')
    search_fields = ('first_name', 'last_name', 'department')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'major', 'credits')
    search_fields = ('name', 'major', 'credits')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'professor', 'building', 'room', 'semester', 'year', 'size')
    search_fields = ('course', 'professor', 'building', 'room', 'semester', 'year', 'size')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'class_day', 'start_time', 'end_time')
    search_fields = ('section', 'class_day', 'start_time', 'end_time')


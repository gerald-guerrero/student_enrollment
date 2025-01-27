from django.contrib import admin
from .models import Student, Professor, Course, Section, Schedule

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'major', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'major', 'enrollment_date')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department')
    search_fields = ('first_name', 'last_name', 'department')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'credits')
    search_fields = ('name', 'credits')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'professor', 'building', 'room', 'semester', 'year')
    search_fields = ('course', 'professor', 'building', 'room', 'semester', 'year')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'class_day', 'start_time', 'end_time')
    search_fields = ('section', 'class_day', 'start_time', 'end_time')


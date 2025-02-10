from django.contrib import admin
from .models import Major, Student, Professor, Course, Section, Schedule, SectionEnrollment

# Register your models here.
@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'semester_enrolled', 'year_enrolled']
    list_display = ('first_name', 'last_name', 'major', 'semester_enrolled', 'year_enrolled')
    search_fields = ('first_name', 'last_name', 'major__title', 'semester_enrolled', 'year_enrolled')
    

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department')
    search_fields = ('first_name', 'last_name', 'department')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'major', 'credits')
    search_fields = ('name', 'major__title', 'credits')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    exclude = ['students']
    list_display = ('course__name', 'professor', 'building', 'room', 'semester', 'year', 'size')
    search_fields = ('course__name', 'professor__first_name', 'professor__last_name', 'building', 'room', 'semester', 'year', 'size')

@admin.register(SectionEnrollment)
class EnrollmentsAdmin(admin.ModelAdmin):
    list_display = ('course', 'id', 'professor','semester', 'year', 'size')
    search_fields = ('course__name', 'id', 'professor__first_name', 'professor__last_name', 'semester', 'year', 'size')
    fields = ['students']
    filter_horizontal = ['students']

    def has_add_permission(self, request):
        return False

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'class_day', 'start_time', 'end_time')
    search_fields = ('section__course__name', 'class_day', 'start_time', 'end_time')


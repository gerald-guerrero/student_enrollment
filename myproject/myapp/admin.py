from django.contrib import admin
from .models import Major, Student, Professor, Course, Section, Schedule, Enrollment

class SectionInline(admin.TabularInline):  
    model = Section
    readonly_fields = ['course', 'professor', 'building', 'room', 'semester', 'year', 'size']
    extra = 0
    can_delete = False
    max_num = 0

class ScheduleInline(admin.TabularInline):  
    model = Schedule
    extra = 0

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
    inlines = [SectionInline]
    list_display = ('first_name', 'last_name', 'department')
    search_fields = ('first_name', 'last_name', 'department')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [SectionInline]
    list_display = ('name', 'major', 'credits')
    search_fields = ('name', 'major__title', 'credits')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    exclude = ['students']
    inlines = [ScheduleInline]
    list_display = ('course__name', 'professor', 'building', 'room', 'semester', 'year', 'size')
    search_fields = ('course__name', 'professor__first_name', 'professor__last_name', 'building', 'room', 'semester', 'year', 'size')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['section', 'student']
    search_fields = ['section__course__name', 'student__first_name', 'student__last_name']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('section', 'class_day', 'start_time', 'end_time')
    search_fields = ('section__course__name', 'class_day', 'start_time', 'end_time')


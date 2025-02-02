from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/update/info', views.StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/update/enrollment', views.EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete')
]
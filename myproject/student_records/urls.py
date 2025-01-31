from django.urls import path
from . import views

urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update'),
]
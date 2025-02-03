from django.urls import path
from . import views

urlpatterns = [
    path('', views.SectionListView.as_view(), name='section_list'),
    path('<int:pk>/', views.SectionDetailView.as_view(), name='section_detail'),
    path('<int:pk>/update', views.SectionUpdateView.as_view(), name='section_update'),
    path('<int:pk>/enroll', views.enroll_section, name="enroll_section"),
]
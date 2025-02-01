from django.urls import path
from . import views

urlpatterns = [
    path('', views.SectionListView.as_view(), name='section_list'),
    path('<int:pk>/', views.SectionUpdateView.as_view(), name='section_update'),
    path('<int:pk>/enroll', views.enroll_section, name="enroll_section"),
    path('<int:pk>/withdraw', views.withdraw_section, name="withdraw_section"),
]
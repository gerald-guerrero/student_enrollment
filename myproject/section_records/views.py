from django.shortcuts import render
from myapp.models import Section
from django.views.generic import ListView

class SectionListView(ListView):
    model = Section
    template_name = 'section_records/section_list.html'
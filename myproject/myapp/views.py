from django.shortcuts import render
from django.contrib.auth.decorators import login_not_required
from rest_framework import viewsets, permissions
from .models import Student
from .serializers import StudentSerializer
from .permissions import StudentAccessPermission

@login_not_required
def homepage(request):
    """
    Basic homepage FBV. Renders index.html template with all features
    accessible from base.html nav bar
    """

    return render(request, "myapp/index.html")

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    permission_classes = [StudentAccessPermission]
    http_method_names = ['get', 'head']
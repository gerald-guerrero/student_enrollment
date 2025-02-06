from django.shortcuts import render
from .models import Section
from django.contrib.auth.decorators import login_not_required

@login_not_required
def homepage(request):
    """
    Basic homepage FBV. Renders index.html template with all features
    accessible from base.html nav bar
    """

    return render(request, "myapp/index.html")
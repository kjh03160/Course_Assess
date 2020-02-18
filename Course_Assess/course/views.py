from django.shortcuts import render, redirect
from .models import Course
from .crwal import crwal_Table

# Create your views here.
def home(request):
    return render(request, 'course.html')

def db_push(request):
    crwal_Table.crwaling('20', '1')
    return redirect('/')
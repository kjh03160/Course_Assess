from django.shortcuts import render
from .models import Course

# Create your views here.
def home(request):
    return render(request, 'course.html')

def db_push(request, dept, name, syllabus, prof, credit, year):
    Course(dept=dept, syllabus=syllabus, name=name, prof=prof, credit=creidt, year=year).save()
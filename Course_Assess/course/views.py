from django.shortcuts import render, redirect
from .models import Course
from .crwal import crwal_Table
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'course.html')

def db_push(request):
    crwal_Table.crwaling('20', '1')
    return redirect('/')

def course_list(request):
    courses = Course.objects.all().order_by('year')
    return render(request, 'post.html', {'courses':courses})

def post_view(request, name, prof):
    course = Course.objects.filter(name=name, prof=prof)[0]
    course_name = course.name
    course_prof = course.prof
    course_dept = course.dept
    course_year = course.year
    course_stars = course.stars
    context = {
        'name' : course_name,
        'prof' : course_prof,
        'dept' : course_dept,
        'year' : course_year,
        'stars' : course_stars,
    }
    return render(request, 'post_detail.html', context)


def post_detail(request, name):
    post = get_object_or_404(Course, pk=name)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=name)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})
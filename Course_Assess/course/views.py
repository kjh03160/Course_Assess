from django.shortcuts import render, redirect
from .models import Course, Assessment
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
    # print(course.comments)
    course_name = course.name
    course_prof = course.prof
    course_dept = course.dept
    course_year = course.year
    course_stars = course.stars
    course_comment = course
    context = {
        'name' : course_name,
        'prof' : course_prof,
        'dept' : course_dept,
        'year' : course_year,
        'stars' : course_stars,
        'post' : course,
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

def search_by_prof(request):
    if request.method == "POST":
        prof = request.POST["prof"]
        courses = Course.objects.filter(prof__contains=prof).order_by('year')
        if len(courses) != 0:
            return render(request, 'post.html', {'courses' : courses})
        else:
            return render(request, 'post.html', {'error':'검색 결과가 없습니다'})
    else:
        return redirect('/')

def search_by_course(request):
    if request.method == "POST":
        name = request.POST["course"]
        courses = Course.objects.filter(name__contains=name).order_by('year')
        if len(courses) != 0:
            return render(request, 'post.html', {'courses' : courses})
        else:
            return render(request, 'post.html', {'error':'검색 결과가 없습니다'})
    else:
        return redirect('/')

def newreply(request):
        if request.method == 'POST':
                comment = Assessment()
                comment.contents = request.POST['comment_body']
                parse = request.POST['blog']
                prof = parse.split('+')[1]
                name = parse.split('+')[0]
                course = Course.objects.get(name = name, prof = prof) 
                comment.course = course                
                comment.post = request.user
                comment.star = request.POST['comment_stars']
                comment.save()

                count = course.count
                course.count += 1
                course.save()
                print(count, course.count)
                if course.stars:
                    course.stars = round(((course.stars * count) + int(comment.star)) / course.count, 2)
                else:
                    course.stars = int(request.POST['comment_stars']) 
                course.save()
                return redirect('/posts/'+ str(comment.course.name)+ '/' + comment.course.prof, {'course' : course})
        else :
                return redirect('/posts') # 홈으로

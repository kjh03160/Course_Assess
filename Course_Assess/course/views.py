from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Assessment
from .crwal import crwal_Table
from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.
def home(request):
    return redirect('auth/')

def db_push(request):
    crwal_Table.crwaling('20', '1')
    return redirect('/')

def course_list(request):
    courses = Course.objects.all().order_by('year')
    return render(request, 'post.html', {'courses':courses})

def post_view(request, name, prof):
    course = Course.objects.get(name=name, prof=prof)
    # print(course.comments)
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
        'post' : course,
    }
    return render(request, 'post_detail.html', context)


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
        try:
            parse = request.POST['blog']
            prof = parse.split('+')[1]
            name = parse.split('+')[0]
            objs = Assessment.objects.get(post=request.user).post
        except:
            comment = Assessment()
            comment.contents = request.POST['comment_body']
            course = Course.objects.get(name = name, prof = prof) 
            comment.course = course                
            comment.post = request.user
            comment.star = request.POST['rating']
            comment.save()

            count = course.count
            course.count += 1
            course.save()
            if course.stars:
                course.stars = round(((course.stars * count) + int(comment.star)) / course.count, 2)
            else:
                course.stars = int(request.POST['rating']) 
            course.save()
            return redirect('/posts/'+ comment.course.name + '/' + comment.course.prof, {'course' : course})

        else:
            print(1)
            return redirect('/posts/'+ name+ '/' + prof, {'error' : '이미 강의평을 등록하셨습니다!'})
    else :
            return redirect('/posts') # 홈으로

def comment_remove(request, pk):
    comment = get_object_or_404(Assessment, pk=pk)
    post = get_object_or_404(Course, name=comment.course.name, prof=comment.course.prof)
    if not comment.post == request.user:
        return HttpResponseRedirect("/posts/{0}/{1}".format(post.name, post.prof))
    else:
        count = post.count
        assess = comment.star
        comment.delete()
        temp = post.stars * count - assess
        count -= 1
        if count != 0:
            post.stars = round(temp / count, 2)
        else:
            post.stars = None
        post.count = count
        post.save()

        return redirect("/posts/{0}/{1}".format(post.name, post.prof))


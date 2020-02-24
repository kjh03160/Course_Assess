from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Assessment
from .crwal import crwal_Table, crwal_Table2
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import CommentForm

# Create your views here.
def home(request):
    return redirect('post')


def setting(request):
    if request.user.is_staff:
        return render(request, 'course.html')
    
    courses = Course.objects.all().order_by('year')
    return render(request, 'post.html', {'courses':courses, 'error' : '접근 권한이 없습니다!'})

def db_push(request):
    year = request.GET.get('year')
    semester = request.GET.get('semester')
    crwal_Table.crwaling(year, semester)
    # crwal_Table2.crwaling(year, semester)
    return redirect('/')

def db_push2(request):
    year = request.GET.get('year2')
    semester = request.GET.get('semester2')
    crwal_Table2.crwaling(year, semester)

    return redirect('/')

def course_list(request):
    courses = Course.objects.all().order_by('year')
    return render(request, 'post.html', {'courses':courses})

def post_view(request, name, prof):
    course = Course.objects.get(name=name, prof=prof)
    
    star_ = None
    if course.stars:
        star_ = course.stars * 20
    
    comments = course.course_comments.all()
    comment_list = []
    for i in comments:
        obj = {}
        obj['user'] = i.post
        obj['star'] = i.star
        obj['star_span'] = int(i.star) * 20
        obj['created_date'] = i.created_date
        obj['contents'] = i.contents
        obj['pk'] = i.pk
        comment_list.append(obj)
    context = {
        'course' : course,
        'comment_list' : comment_list,
        'star_' : star_
    }
    return render(request, 'post_detail.html', context)


def search(request):
    if request.method == "POST":
        q = request.POST["q"]
        courses = Course.objects.filter(Q(prof__contains=q) | Q(name__contains=q)).order_by('year')
        if len(courses) != 0:
            return render(request, 'post.html', {'courses' : courses})
        else:
            return render(request, 'post.html', {'error':'검색 결과가 없습니다'})
    else:
        return redirect('/')


def newreply(request):
    if request.method == 'POST':
        parse = request.POST['blog']
        prof = parse.split('+')[1]
        name = parse.split('+')[0]
        course = Course.objects.get(name = name, prof = prof)
        try:
            objs = Assessment.objects.get(post=request.user, course=course).post
        except:
            comment = Assessment()
            comment.contents = request.POST['comment_body']
            comment.course = course                
            comment.post = request.user
            comment.star = request.POST['rating']
            comment.save()

            count = course.count
            if count:
                course.count += 1
            else:
                course.count = 1
            course.save()
            if course.stars:
                course.stars = round(((course.stars * count) + int(comment.star)) / course.count, 2)
            else:
                course.stars = int(request.POST['rating']) 
            course.save()
            return redirect('/posts/'+ comment.course.name + '/' + comment.course.prof)

        else:
            context = {
                'course' : course,
                'error' : '이미 강의평을 등록하셨습니다!'
                }
            return render(request, 'post_detail.html', context)
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


def comment_update(request, pk):
    comment = get_object_or_404(Assessment, pk=pk)
    course = comment.course
    prof = comment.course.prof
    name = comment.course.name
    star_ = course.stars * 20

    if request.method == "POST":
        before = course.stars
        after = request.POST['rating']
        comment.star = request.POST['rating']
        comment.contents = request.POST['comment_body']
        course.stars = round(((course.stars * course.count) - before + int(after)) / course.count, 2)
        course.save()
        comment.save()
        return redirect('detail', name = name, prof = prof)
    else:
        stars = comment.star
        content = comment.contents
    
    return render(request, 'comment_update.html', { 'course' : course, 'star_' : star_, 'stars' : stars, 'content' : content})



from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup_page(request):
    return render(request, 'signup.html')

def signup(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["password2"] and len(request.POST["username"])==9:
            try:
                user = User.objects.create_user(
                    username = request.POST["username"],
                    password = request.POST["password"]
                )
                auth.login(request, user)
                return redirect('/')
            except:
                return render(request, 'signup.html', {'error':'이미 존재하는 학번입니다.'})

        else:
            return render(request, 'signup.html', {'error':'학번이 잘못되었거나 비밀번호가 일치하지 않습니다'})
    
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('post')
        else:
            return render(request, 'home.html', {'error':'학번 혹은 패스워드가 틀렸습니다'})
    else:
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


        


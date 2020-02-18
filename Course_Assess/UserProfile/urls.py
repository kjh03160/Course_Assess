from django.urls import path
from UserProfile import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('signup_page', views.signup_page, name="signup_page")
]
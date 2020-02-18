from django.contrib import admin
from django.urls import path
from course import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]

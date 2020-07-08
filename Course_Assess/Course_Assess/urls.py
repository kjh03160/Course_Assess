from django.contrib import admin
from django.urls import path, include
from course import views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('course', include('course.urls')),

    # 유저계정
    path('auth/', include('UserProfile.urls'))
]

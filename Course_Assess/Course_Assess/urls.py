from django.contrib import admin
from django.urls import path, include
from course import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('crwal', views.db_push, name='crwal'),


    # 유저계정
    path('auth/', include('UserProfile.urls'))
]

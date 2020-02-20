from django.contrib import admin
from django.urls import path, include
from course import views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('crwal/', views.db_push, name='crwal'),
    path('posts', views.course_list, name='post'),
    url(r'^posts/(?P<name>.+)/(?P<prof>.+)/$', views.post_view, name='detail'),
    path('posts_search_by_prof', views.search_by_prof, name='prof'),
    path('posts_search_by_course', views.search_by_course, name='course'),
    path('posts/newreply',views.newreply, name="newreply"),
    # url(r'^posts/(?P<name>.+)/(?P<prof>.+)/remove/(?P<pk>\d+)/$', views.comment_remove, name='comment_remove'),
    path('remove/<int:pk>',views.comment_remove, name='remove'),


    # 유저계정
    path('auth/', include('UserProfile.urls'))
]

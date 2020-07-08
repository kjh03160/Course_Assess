from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url
urlpatterns = [
    path('setting/', views.setting, name='setting'),
    path('crwal/', views.db_push, name='crwal'),
    path('crwal2/', views.db_push2, name='crwal2'),

    path('', views.course_list, name='post'),
    url(r'^posts/(?P<name>.+)/(?P<prof>.+)/$', views.post_view, name='detail'),
    path('search', views.search, name='search'),
    path('update/<int:pk>', views.comment_update, name='update'),

    path('newreply',views.newreply, name="newreply"),
    path('remove/<int:pk>',views.comment_remove, name='remove'),
]

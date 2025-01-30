from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('home/', views.home, name='home'),
    path('settings/', views.settings, name="settings"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('search/', views.search, name="Search"),
    path('home/addPost', views.addPost, name="Add New Post"),
    path('home/addComment', views.addComment, name="Add New Post"),
    path('post/<int:id>', views.displayPost, name="display post"),
    path('logout/', views.logout, name="logout"),
    
]

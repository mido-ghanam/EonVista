from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.http import HttpResponse
from . import models

def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Authentication, Please check your Username or Password')
            return redirect('login')
    else:
        return render(request, 'login_register.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=firstname,
                    last_name=lastname
                )
                user.save()
                messages.success(request, 'User registered successfully!\n Please login now')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    else:
        return render(request, 'login_register.html')

@login_required
def home(request):
    feeds = models.addPost.objects.all().order_by('-created_at')
    comments = models.addComment.objects.all()
    return render(request, 'home.html', {
        'user': request.user,
        'feeds': feeds,
        'comments': comments,
    })
    
def settings(request):
    return render(request, 'settings.html')

@login_required
def search(request):
    query = request.GET.get('q')
    results = {'users': [], 'groups': []}
    if query:
        results['users'] = User.objects.filter(
            username__icontains=query
        ) | User.objects.filter(
            first_name__icontains=query
        ) | User.objects.filter(
            last_name__icontains=query
        )
        results['groups'] = Group.objects.filter(name__icontains=query)
    return render(request, 'search.html', {'results': results, 'query': query})

@login_required
def addPost(request):
    if request.method == 'POST':
        post_body = request.POST.get('postbody')
        if post_body.strip() == '':
            messages.error(request, 'Post content cannot be empty.')
        else:
            models.addPost.objects.create(publisher=request.user, body=post_body)
            messages.success(request, 'Post created successfully!')
    return redirect('home')

@login_required
def addComment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_body = request.POST.get('comment_body')
        if comment_body.strip() == '':
            messages.error(request, 'Comment content cannot be empty.')
        else:
            post = models.addPost.objects.get(id=post_id)
            models.addComment.objects.create(post=post, user=request.user, body=comment_body)
            messages.success(request, 'Comment added successfully!')
    return redirect('home')

@login_required
def displayPost(request, id):
    post = models.addPost.objects.get(id=id)
    comments = models.addComment.objects.filter(post=post)
    return render(request, 'displayPost.html', {'post': post, 'comments': comments,})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

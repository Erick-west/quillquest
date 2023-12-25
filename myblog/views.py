from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

def blog_new(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')  # No content limit
        date_posted = timezone.now()

        Blog.objects.create(title=title, content=content, date_posted=date_posted)
        return redirect('blog:blog_list')

    return render(request, 'blog_edit.html', {'edit_mode': False})

def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')  # No content limit
        blog.save()
        return redirect('blog:blog_list')

    return render(request, 'blog_edit.html', {'edit_mode': True, 'blog': blog})

def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect('blog:blog_dashboard')

@login_required(login_url='blog:login')
def blog_dashboard(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_dashboard.html', {'blogs': blogs})

from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            # Handle the case where the username already exists (you can redirect to an error page or display a message)
            return render(request, 'signup.html', {'error_message': 'Username already exists'})

        # Create a new user
        user = User.objects.create_user(username=username, password=password)

        # Authenticate and log in the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('blog:blog_dashboard')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('blog:blog_dashboard')
    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('blog:blog_list')

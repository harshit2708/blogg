from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User,Blog
from django.urls import reverse
from blog.functions import handle_uploaded_file

# Create your views here.

def index(request):
	return render(request, 'blog/index.html')

@login_required
def blogs(request):
    blogs = Blog.objects.all()    
    print(blogs)
    return render(request, 'blog/blogs.html',{
        "blogs" : blogs
        })

@login_required
def read(request, id):
    blog = Blog.objects.filter(blog_id = id)[0]
    return render(request, 'blog/read.html',{
        'blog' : blog
        })

@login_required
def myblogs(request):
    my_blogs = Blog.objects.filter(user = request.user.username)
    print(my_blogs)
    return render(request, 'blog/myblogs.html',{
        "my_blogs" : my_blogs
        })

@login_required
def write(request):
    if request.method == "POST" and request.FILES["image"]:
        # Attempt to sign user in
        user = request.user.username
        category = request.POST["category"]
        title = request.POST["title"]
        content = request.POST["content"]
        image = request.FILES["image"]
        
        blog = Blog(user = user, category = category,title = title, content= content, image = image)
        blog.save()
       
    else:
        return render(request, "blog/write.html")
    return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "blog/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "blog/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "blog/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "blog/register.html")

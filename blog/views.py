from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User,Blog,Comment
from django.urls import reverse
from blog.functions import handle_uploaded_file
from django.db.models import Count
from math import ceil

# Create your views here.

def index(request):
    return render(request, 'blog/index.html')



def blogs(request):
    blogs = Blog.objects.all()
    technology_blogs = Blog.objects.filter(category = "Technology").order_by('-pub_date')
    n = len(technology_blogs[0:4])
    print(n)
    nSlides = n//4 + ceil((n / 4) - (n //4))
    print(blogs)
    return render(request, 'blog/blogs.html',{
        "blogs" : blogs,
        "technology_blogs" : technology_blogs,
        "range" : range(1 , nSlides),
        "nSlides" : nSlides
        })


@login_required
def read(request, id):
    message = False
    post = Blog.objects.get(pk = id)
    post.views.add(User.objects.get(username = request.user.username))

    print("hii")
    blog = Blog.objects.filter(blog_id = id)[0]
    comments = Comment.objects.filter(blog_id = id).order_by('-date')
    if len(comments) == 0:
        message = True
    if request.method == "POST":
        comment = request.POST["comment"]
        comment = Comment(blog_id = id, comment_by = request.user.first_name, comment = comment)
        comment.save()
    else:
        return render(request,'blog/read.html',{'blog' : blog, 'comments' : comments,'message' : message})
  

    return HttpResponseRedirect('%d' %id)


@login_required
def myblogs(request):
    check = False
    my_blogs = Blog.objects.filter(user = request.user.username)
    if len(my_blogs) == 0:
        check = True
    return render(request, 'blog/myblogs.html',{
        "my_blogs" : my_blogs,
        "check" : check
        })


@login_required
def edit_blog(request,id):
    if request.method == "POST":
        blog_id = id
        user = request.user.username
        user_name = request.user.first_name
        category = request.POST["category"]
        title = request.POST["title"]
        content = request.POST["content"]
        image = request.FILES.get('image', False)
        blog = Blog.objects.filter(pk = id)[0]
        pub_date = blog.pub_date
        if(image == False):
            image = blog.image
            blog = Blog(blog_id = blog_id,user = user, user_name = user_name, category = category, title = title, content = content, image = image, pub_date = pub_date)
        else:
            image = request.FILES["image"]
            blog = Blog(blog_id = blog_id,user = user, user_name = user_name, category = category, title = title, content = content, image = image, pub_date = pub_date)
        blog.save()

    elif request.method == "POST":
        # Attempt to sign user in
        user = request.user.username
        user_name = request.user.first_name
        category = request.POST["category"]
        title = request.POST["title"]
        content = request.POST["content"]
      
        blog = Blog(user = user, user_name = user_name, category = category,title = title, content= content)
        blog.save()

    else:
        blog = Blog.objects.filter(pk = id)[0]
        edit = True
        return render(request,'blog/write.html',{
            "edit" : edit,
            "blog" : blog 
            })
    return HttpResponseRedirect(reverse("myblogs"))


@login_required
def delete_blog(request,id):
    if request.method == "POST":
        pi = Blog.objects.get(pk = id)
        pi.delete()
        return HttpResponseRedirect(reverse("myblogs")) 

def contributors(request):
    results = (Blog.objects.values('user_name', 'user')).annotate(bcount = Count('user_name')).order_by('-bcount')
    print(results)
    return render(request, "blog/contributors.html", {'results': results})

@login_required
def write(request):
    if request.method == "POST" and request.FILES["image"]:
        # Attempt to sign user in
        user = request.user.username
        user_name = request.user.first_name
        category = request.POST["category"]
        title = request.POST["title"]
        content = request.POST["content"]
        image = request.FILES["image"]

        blog = Blog(user = user, user_name = user_name, category = category,title = title, content= content, image = image)
        blog.save()
    else:
        return render(request, "blog/write.html", {
            "edit" : False
            })
    return HttpResponseRedirect(reverse("myblogs"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
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
            user = User.objects.create_user(first_name = username, username = email, password = password)
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
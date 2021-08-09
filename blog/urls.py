from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    #path("accounts/", include('django.contrib.auth.urls')),
    path("blogs/",views.blogs, name = "blogs"),
    path("read/<int:id>",views.read, name = "read"),
    path("write/",views.write, name = "write"),
    path("myblogs/",views.myblogs, name = "myblogs"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]
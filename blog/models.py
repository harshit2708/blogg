from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Blog(models.Model):
    blog_id = models.AutoField(primary_key = True)
    user = models.CharField(max_length = 50)
    user_name = models.CharField(max_length = 50, default = "")
    category = models.CharField(max_length = 50)
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 10000)
    pub_date = models.DateField(auto_now_add=True)
    image = models.FileField(upload_to='blog/images', default="")
    views = models.ManyToManyField(User,related_name = "post_views", default = 0)

    def total_views(self):
        return self.views.count()
 
class Comment(models.Model):
    blog_id = models.CharField(max_length = 4)
    comment_by = models.CharField(max_length = 50)
    comment = models.CharField(max_length = 10000)
    date = models.DateTimeField(auto_now_add = True)


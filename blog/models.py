from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Blog(models.Model):
    blog_id = models.AutoField(primary_key = True)
    user = models.CharField(max_length = 50)
    category = models.CharField(max_length = 50)
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 10000)
    pub_date = models.DateField(auto_now_add=True)
    image = models.FileField(upload_to='blog/images', default="")
 
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

class User(AbstractUser):
    icon = models.ImageField(verbose_name='img',upload_to="uploads/",default="images/noimage.png")

class Talk(models.Model):
    send_from = models.IntegerField()
    send_to = models.IntegerField()
    message = models.TextField(max_length = 1000)
    date = models.DateTimeField(default=datetime.datetime.now())

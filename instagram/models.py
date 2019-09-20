from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    following = models.ManyToManyField('self', blank = True)
    def __str__(self):
        return self.username

class Post(models.Model):
    photo = models.ImageField(blank=False, null=False)
    text = models.CharField(max_length=300)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null = True)
    def __str__(self):
        return self.text[:15]

from time import time

from django.contrib.auth.models import User
from django.db import models


def get_upload_file_name(instance, filename):
    return '%s_%s' % (str(time()).replace('.', '_'), filename)


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Advert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField()
    price = models.IntegerField(null=False)
    image = models.FileField(upload_to=get_upload_file_name, null=True, blank=True)
    location = models.CharField(max_length=50, null=False)
    pub_date = models.DateField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    text = models.TextField(null=False)

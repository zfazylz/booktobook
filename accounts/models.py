from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    DOB = models.DateField(null=True)
    public_email = models.EmailField(null=True)
    county = models.CharField(max_length=20, null=True)
    town = models.CharField(max_length=30, null=True)


class PersonalMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    text = models.TextField(null=False)
    sent_date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
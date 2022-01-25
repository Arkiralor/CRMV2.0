from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass


class AgentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=128)
    fname = models.CharField(max_length=64, null=True)
    lname = models.CharField(max_length=64, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __init__(self, user: User):
        self.user = user
        self.fname = self.user.username
        self.fname = self.user.first_name
        self.lname = self.user.last_name

    def __str__(self):
        return self.user.username

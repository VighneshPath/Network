from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    """
        Members:
            user: References the User Class
            content: Text
            time_stamp: Date and Time
            likes: Integer
    """
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posts")

    content = models.CharField(max_length=128)

    time_stamp = models.DateField(auto_now = False, auto_now_add = True)

    likes = models.IntegerField()

class Follow(models.Model):
    """
        Members:
            follower: References the User Class
            following: References the User Class
    """

    follower = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "following")
    following = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "follower")

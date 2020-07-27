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

    time_stamp = models.DateTimeField(auto_now = False, auto_now_add = True)

    likes = models.IntegerField(default = 0)

    def __str__(self):
        return f"By: {self.user}\nContent: {self.content}\nPosted: {self.time_stamp}\nLikes: {self.likes}"

class Follow(models.Model):
    """
        Members:
            follower: References the User Class
            following: References the User Class
    """

    follower = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "following")
    following = models.ForeignKey(User, on_delete = models.PROTECT, related_name = "follower")

    def __str__(self):
        return f"{self.follower} is following {self.following}"


class Like(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "liked_by")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "liked_post")

    def __str__(self):
        return f"{self.user} Liked {self.post}"

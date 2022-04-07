from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class NetworkUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="networks")
    follower = models.ManyToManyField(User, blank=True, related_name="follower_users")
    following = models.ManyToManyField(User, blank=True, related_name="following_users")

    def __str__(self):
        return f"NetUser {self.user}"

class Post(models.Model):
    title = models.CharField(max_length=64)
    body = models.TextField(blank=True)
    user = models.ForeignKey(NetworkUser, on_delete=models.CASCADE, related_name="posts")
    like = models.ManyToManyField(NetworkUser,blank=True, related_name="likes")
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.title} {self.user}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "like": [user.user.username for user in self.like.all()],
            "created": datetime.strftime(self.created,"%B %d, %Y %H:%M:%S"),
            "nlikes": self.like.all().count(),
            "user":self.user.user.username
        }

class Comment(models.Model):
    text = models.TextField(max_length=255)
    user = models.ForeignKey(NetworkUser, on_delete=models.CASCADE, related_name="my_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user} {self.text}"
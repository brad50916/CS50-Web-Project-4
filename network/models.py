from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(default="", max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post", null=True)
    date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)

    def serialize(self):
        return {
            "content": self.content,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like
        }

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="r_user", null=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="r_following", null=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="r_post", null=True)
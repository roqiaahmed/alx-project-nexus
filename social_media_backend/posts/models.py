from django.db import models
from django.conf import settings


class ReactionStatus(models.TextChoices):
    Like = "LIKE", "Like"
    Dislike = "DISLIKE", "Dislike"
    Love = "LOVE", "Love"


# Create your models here.
class Post(models.Model):
    content_text = models.TextField(null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reaction(models.Model):
    states = models.CharField(
        choices=ReactionStatus.choices,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content_text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

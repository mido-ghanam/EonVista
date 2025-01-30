from django.db import models
from django.contrib.auth.models import User

class addPost(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class addComment(models.Model):
    post = models.ForeignKey(addPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


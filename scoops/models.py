import uuid
from django.db import models
from django.contrib.auth.models import User    

# Create your models here.

class Scoop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    scoop = models.ForeignKey(Scoop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        unique_together = ['author', 'scoop']
    def __str__(self):
        return "Like"        
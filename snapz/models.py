import uuid
from django.db import models
from django.contrib.auth.models import User         

# Create your models here.
class Snapz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=150)
    image = models.ImageField(upload_to="snapz_image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
    
class Comment(models.Model):    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    snapz = models.ForeignKey(Snapz, on_delete=models.CASCADE)
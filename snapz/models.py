import uuid
from django.db import models
from django.contrib.auth.models import User       

# Create your models here.
class Snapz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
    
class SnapzImage(models.Model):
    image = models.ImageField(upload_to="snapz_image")
    snapz = models.ForeignKey(Snapz, on_delete=models.CASCADE, related_name="images" )

class Comment(models.Model):    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    snapz = models.ForeignKey(Snapz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.content

class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    snapz = models.ForeignKey(Snapz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        unique_together = ['author', 'snapz']
    def __str__(self):
        return "Like"    
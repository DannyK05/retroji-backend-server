from django.contrib import admin
from .models import Snapz, Comment

# Register your models here.
admin.site.register([Snapz, Comment])
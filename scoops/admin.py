from django.contrib import admin
from .models import Scoop, Like


# Register your models here.
admin.site.register([Like, Scoop])
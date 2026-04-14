from django.urls import path
from search import views
urlpatterns = [path('', view=views.search, name='search')]
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name= 'register'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name='logout'),
    path('username/<str:username>', views.is_username_taken, name='is_username_taken')
]
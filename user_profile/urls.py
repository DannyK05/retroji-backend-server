from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>/", views.get_user_profile, name='get_user_profile'),
    path("snapz/", views.get_user_snapz, name='get_user_snapz'),
    path("scoops/", views.get_user_scoops, name='get_user_scoops'),
    path("comments/", views.get_user_comments, name='get_user_comments'),
    path("update/", views.update_user_profile, name='update_user_profile'),
    path("follow/", views.follow_user_profile, name='follow_user_profile'),
]
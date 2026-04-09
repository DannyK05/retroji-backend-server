from django.urls import path
from . import views

urlpatterns = [
    path("<int:user_id>", views.get_user_profile, name='get_user_profile'),
    path("update/", views.update_user_profile, name='update_user_profile'),
    path("follow/", views.follow_user_profile, name='follow_user_profile'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_scoops, name="get_all_scoops"),
    path('<uuid:parent_id>/', views.get_all_scoops_replies_by_id, name="get_all_scoops_by_id"),
    path('post/', views.post_scoops, name="post_scoops"),
    path('like/', views.like_scoops, name="like_scoops"),
]
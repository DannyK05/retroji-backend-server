from django.urls import path
from . import views

urlpatterns = [
    # Snapz
    path('', views.get_all_snapz, name="get_all_snapz"),
    path('post/', views.post_snapz, name="post_snapz"),
    path('<uuid:snapz_id>/', views.get_snapz_by_id, name="get_snapz_by_id"),
    path('delete/', views.delete_snapz, name="delete_snapz"),

    # Comments
    path('<uuid:snapz_id>/comments/', views.get_all_comments_by_snapz_id, name="get_all_comments_by_snapz_id"),
    path('comment/post/', views.post_comment, name="post_comment"),
    path('comment/delete/', views.delete_comment, name="delete_comment"),

    # Likes
    path('like/', views.like, name="like_post"),
]
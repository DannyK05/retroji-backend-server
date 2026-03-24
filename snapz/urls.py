from django.urls import path
from . import views

urlpatterns = [
    # Snapz
    path('snapz/', views.get_all_snapz, name="get_all_snapz"),
    path('snapz/post/', views.post_snapz, name="post_snapz"),
    path('snapz/<uuid:snapz_id>/', views.get_snapz_by_id, name="get_snapz_by_id"),

    # Comments
    path('snapz/<uuid:snapz_id>/comments/', views.get_all_comments_by_snapz_id, name="get_all_comments_by_snapz_id"),
    path('snapz/comment/post/', views.post_comment, name="post_comment"),

    # Likes
    path('snapz/like/', views.like, name="like_post"),
]
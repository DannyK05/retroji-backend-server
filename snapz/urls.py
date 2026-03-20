from django.urls import path
from . import views

urlpatterns = [
    # Snapz
    path('snapz/', views.get_all_snapz),
    path('snapz/post/', views.post_snapz),
    path('snapz/<uuid:snapz_id>/', views.get_snap_by_id),

    # Comments
    path('snapz/<uuid:snapz_id>/comments/', views.get_all_comment_by_snapz_id),
    path('snapz/comment/post/', views.post_comment),

    # Likes
    path('snapz/like/', views.like),
]
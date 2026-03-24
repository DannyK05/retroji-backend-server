from rest_framework import serializers
from .models import Snapz, Comment


class SnapzSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Snapz
        fields = ["id","image","caption", "author", "like_count", "comment_count", "created_at", "updated_at"]
    
    def get_like_count (self, obj):
        return obj.like_set.count()
    
    def get_comment_count (self, obj):
        return obj.comment_set.count()
    
    
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "content","snapz","created_at"]

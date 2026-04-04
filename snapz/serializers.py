from rest_framework import serializers
from .models import Snapz, Comment, Like
from accounts.serializers import UserSerializer


class SnapzSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    is_liked= serializers.SerializerMethodField()

    class Meta:
        model = Snapz
        fields = ["id","image","caption", "author", "like_count", "comment_count", "is_liked", "created_at", "updated_at"]
    
    def get_like_count (self, obj):
        return obj.like_set.count()
    
    def get_comment_count (self, obj):
        return obj.comment_set.count()
    
    def get_is_liked (self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(author=request.user, snapz=obj).exists()
        else:
            return False
    
    
    
        

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ["author", "content","snapz","created_at"]

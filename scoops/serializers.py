from rest_framework import serializers
from .models import Scoop, Like
from accounts.serializers import UserSerializer

class ScoopSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Scoop
        fields = ["id", "author", "content", "parent", "replies", "is_liked", "like_count", "replies_count","created_at", "updated_at"]

    def get_replies(self, obj):
        replies = obj.replies.all()
        return ScoopSerializer(replies, many=True, context=self.context).data

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(author=request.user, scoop=obj).exists()
        return False

    def get_like_count(self, obj):
        return obj.like_set.count()
    
    def get_replies_count(self,obj):
        return obj.replies.count()
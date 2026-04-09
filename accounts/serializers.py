from rest_framework import serializers 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    class Meta:
        model = User 
        fields = ["id", "username", "email", "following", "followers"]

    def get_following(self, obj):
        return obj.following.count()
    
    def get_followers(self, obj):
        return obj.followers.count()
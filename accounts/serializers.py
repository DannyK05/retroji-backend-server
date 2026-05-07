from rest_framework import serializers 
from django.contrib.auth.models import User
from user_profile.models import Profile

class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = User 
        fields = ["id", "username", "following", "followers", "image"]

    def get_following(self, obj):
        return obj.following.count()
    
    def get_followers(self, obj):
        return obj.followers.count()
    
    def get_image(self, obj):
        try:
            profile = Profile.objects.get(user=obj)
            if profile.image and profile.image.name:
                return profile.image.url
            return None
        except Profile.DoesNotExist:
            return None
            

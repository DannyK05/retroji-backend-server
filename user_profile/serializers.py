from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Profile, Follow

class ProfileSerializer (serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_followed = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ["user", "id", "image","is_followed", "created_at", "updated_at"]

    def get_is_followed (self, obj) :
        request = self.context.get('request')
        return Follow.objects.filter(following=obj.user.id, follower=request.user.id).exists()
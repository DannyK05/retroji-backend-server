from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Profile

class ProfileSerializers (serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ["user", "id", "image", "created_at", "updated_at"]
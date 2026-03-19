from rest_framework import serializers
from .models import Snapz

class SnapzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapz
        fields = ["id","image","caption", "author", "created_at", "updated_at"]
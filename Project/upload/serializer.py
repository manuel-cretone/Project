from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

class MySerializer(serializers.Serializer):
    # name = serializers.CharField()
    file = serializers.FileField()
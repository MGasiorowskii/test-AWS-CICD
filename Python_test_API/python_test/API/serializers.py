from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class CreateUpdateSerializer(serializers.ModelSerializer):
    url = serializers.URLField()

    class Meta:
        model = Photo
        fields = ['title', 'albumId', 'url']

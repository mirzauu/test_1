from rest_framework import serializers
from .models import UploadedImage, ImageDescription

class ImageDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageDescription
        fields = ['tone', 'description']

class UploadedImageSerializer(serializers.ModelSerializer):
    descriptions = ImageDescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = UploadedImage
        fields = ['id', 'image', 'uploaded_at', 'image_url', 'descriptions']
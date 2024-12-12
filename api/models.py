from django.db import models

# Create your models here.

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)

class ImageDescription(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='descriptions')
    tone = models.CharField(max_length=50)  
    description = models.TextField()
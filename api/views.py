import base64
import mimetypes
import os
import re
import requests

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .models import UploadedImage, ImageDescription
from .serializers import UploadedImageSerializer


class ImageUploadView(APIView):
  
    parser_classes = [MultiPartParser, FormParser]

    @staticmethod
    def clean_description(description):
  
        description = re.sub(r'\n+', ' ', description).strip()
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', description)
        return ' '.join(sentences[:2])

    def post(self, request, *args, **kwargs):
        
        file = request.data.get('image')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the image
        image = UploadedImage.objects.create(image=file)
        image.image_url = f"{settings.AWS_STORAGE_BUCKET_NAME}/{image.image.name}"
        image.save()

        # Retrieve Gemini API key
        gemini_api_key = settings.GEMINI_API_KEY
        if not gemini_api_key:
            return Response(
                {'error': 'Gemini API key not configured'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Prepare the image for Gemini API
            with image.image.open('rb') as img_file:
                image_data = img_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')

            mime_type = mimetypes.guess_type(image.image.name)[0] or 'image/jpeg'
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_api_key}"
            headers = {'Content-Type': 'application/json'}

            tones = ['formal', 'humorous', 'critical']
            descriptions = {}

            for tone in tones:
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"Generate a {tone} description for this image. Describe what you see in detail."
                                },
                                {
                                    "inlineData": {
                                        "mimeType": mime_type,
                                        "data": base64_image
                                    }
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "maxOutputTokens": 256,
                        "temperature": 0.4
                    }
                }

                response = requests.post(gemini_url, headers=headers, json=payload)

                if response.status_code != 200:
                    return Response(
                        {'error': 'Gemini API request failed', 'details': response.text},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                response_json = response.json()

                try:
                    content = response_json['candidates'][0]['content']['parts'][0]['text']
                    cleaned_content = self.clean_description(content)
                    descriptions[tone] = cleaned_content

                    ImageDescription.objects.create(image=image, tone=tone, description=content)

                except (KeyError, IndexError):
                    return Response(
                        {'error': 'Failed to parse Gemini API response', 'response': response.text},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            return Response(
                {
                    "id": image.id,
                    "image": image.image.url,
                    "descriptions": descriptions
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as error:
            return Response(
                {'error': 'Unexpected error occurred', 'details': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

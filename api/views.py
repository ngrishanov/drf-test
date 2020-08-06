from rest_framework import generics

from api.serializers import (
    ImageUploadSerializer,
    ImageInternalSerializer,
    ImageExternalSerializer,
)
from api.models import Image


class ImageUploadView(generics.CreateAPIView):
    serializer_class = ImageUploadSerializer


class ImageAnnotationView(generics.RetrieveUpdateAPIView):
    lookup_url_kwarg = 'image_uuid'
    queryset = Image.objects.all()

    def get_serializer_class(self):
        annotation_format = self.request.query_params.get('annotation_format', 'internal')

        if annotation_format == 'external' and self.request.method == 'GET':
            return ImageExternalSerializer

        return ImageInternalSerializer

from rest_framework import viewsets, serializers
from raterapi.models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['id', 'image', 'uploaded_at']

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer
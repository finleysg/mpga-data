from rest_framework import viewsets
from .models import Document, Photo
from .serializers import DocumentDetailSerializer, PhotoDetailSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentDetailSerializer
    queryset = Document.objects.all()


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoDetailSerializer
    queryset = Photo.objects.all()

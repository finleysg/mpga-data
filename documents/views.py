from rest_framework import viewsets
from .models import *
from .serializers import *


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        """ Optionally filter by code
        """
        queryset = Document.objects.all()
        year = self.request.query_params.get('year', None)
        tournament = self.request.query_params.get('tournament', None)
        doc_type = self.request.query_params.get('type', None)

        if year is not None:
            queryset = queryset.filter(year=year)
        if tournament is not None:
            queryset = queryset.filter(tournament=tournament)
        if doc_type is not None:
            queryset = queryset.filter(document_type=doc_type)

        return queryset


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        """ Optionally filter by code
        """
        queryset = Photo.objects.all()
        year = self.request.query_params.get('year', None)
        tournament = self.request.query_params.get('tournament', None)
        pic_type = self.request.query_params.get('type', None)

        if year is not None:
            queryset = queryset.filter(year=year)
        if tournament is not None:
            queryset = queryset.filter(event=tournament)
        if pic_type is not None:
            queryset = queryset.filter(photo_type=pic_type)

        return queryset

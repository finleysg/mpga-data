from events.models import Event
from .models import Document, Photo
from rest_framework import serializers


class DocumentSerializer(serializers.ModelSerializer):

    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = Document
        fields = ("id", "year", "title", "document_type", "file", "event", "last_update", )


class PhotoSerializer(serializers.ModelSerializer):

    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = Photo
        fields = ("id", "year", "title", "photo_type", "file", "event", "last_update", )

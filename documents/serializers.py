from events.models import Tournament
from .models import *
from rest_framework import serializers


class DocumentTagSerializer(serializers.ModelSerializer):

    tag = serializers.CharField(source="tag.name")

    class Meta:
        model = DocumentTag
        fields = ("id", "tag", )


class PhotoTagSerializer(serializers.ModelSerializer):

    tag = serializers.CharField(source="tag.name")

    class Meta:
        model = PhotoTag
        fields = ("id", "tag", )


class DocumentSerializer(serializers.ModelSerializer):

    tournament = serializers.PrimaryKeyRelatedField(queryset=Tournament.objects.all(), required=False)
    tags = DocumentTagSerializer(many=True)

    class Meta:
        model = Document
        fields = ("id", "year", "title", "document_type", "file", "tournament", "created_by", "last_update", "tags", )


class PhotoSerializer(serializers.ModelSerializer):

    tournament = serializers.PrimaryKeyRelatedField(queryset=Tournament.objects.all(), required=False)
    tags = PhotoTagSerializer(many=True)

    class Meta:
        model = Photo
        fields = ("id", "year", "caption", "photo_type", "file", "tournament", "thumbnail_image", "web_image",
                  "created_by", "last_update", "tags", )

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

    tags = DocumentTagSerializer(many=True, required=False)

    class Meta:
        model = Document
        fields = ("id", "year", "title", "document_type", "file", "tournament", "created_by", "last_update", "tags", )

    def create(self, validated_data):
        tags = self.context["request"].data.get("tags", None)
        tournament = validated_data.get("tournament", None)
        year = validated_data.pop("year")
        title = validated_data.pop("title")
        document_type = validated_data.pop("document_type")
        file = validated_data.pop("file")
        created_by = self.context["request"].user

        doc = Document(year=year, title=title, document_type=document_type, file=file, tournament=tournament, created_by=created_by)
        doc.save()

        for tag in tags.split("|"):
            t, created = Tag.objects.get_or_create(name=tag)
            dt = DocumentTag(document=doc, tag=t)
            dt.save()

        return doc


class PhotoSerializer(serializers.ModelSerializer):

    thumbnail_url = serializers.ReadOnlyField(source="thumbnail_image.url")
    image_url = serializers.ReadOnlyField(source="web_image.url")
    tags = PhotoTagSerializer(many=True, required=False)

    class Meta:
        model = Photo
        fields = ("id", "year", "caption", "photo_type", "tournament", "thumbnail_url", "image_url", "raw_image",
                  "created_by", "last_update", "tags", )

    def create(self, validated_data):
        tags = self.context["request"].data.get("tags", None)
        tournament = validated_data.get("tournament", None)
        year = validated_data.pop("year")
        caption = validated_data.get("caption", None)
        photo_type = validated_data.pop("photo_type")
        raw_image = validated_data.pop("raw_image")
        created_by = self.context["request"].user

        pic = Photo(year=year, caption=caption, photo_type=photo_type, raw_image=raw_image, tournament=tournament, created_by=created_by)
        pic.save()

        for tag in tags.split("|"):
            t, created = Tag.objects.get_or_create(name=tag)
            pt = PhotoTag(document=pic, tag=t)
            pt.save()

        return pic

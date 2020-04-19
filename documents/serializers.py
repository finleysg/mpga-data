from .models import *
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", )


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
    # tournament = serializers.IntegerField(required=False, allow_null=True)
    created_by = serializers.CharField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

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
        created_by = "test"  # self.context["request"].user

        doc = Document(year=year, title=title, document_type=document_type, file=file, tournament=tournament, created_by=created_by)
        doc.save()

        if tags is not None:
            for tag in tags.split("|"):
                t, created = Tag.objects.get_or_create(name=tag)
                dt = DocumentTag(document=doc, tag=t)
                dt.save()

        return doc

    def update(self, instance, validated_data):
        tags = self.context["request"].data.get("tags", None)

        instance.tournament = validated_data.get("tournament", instance.tournament)
        instance.year = validated_data.get("year", instance.year)
        instance.title = validated_data.get("title", instance.title)
        instance.document_type = validated_data.get("document_type", instance.document_type)
        new_file = validated_data.get("file", None)
        if new_file is not None:
            instance.file = new_file

        instance.save()

        # Delete and recreate tags.
        DocumentTag.objects.filter(document=instance).delete()
        if tags is not None:
            for tag in tags.split("|"):
                t, created = Tag.objects.get_or_create(name=tag)
                dt = DocumentTag(document=instance, tag=t)
                dt.save()

        return instance


class PhotoSerializer(serializers.ModelSerializer):

    thumbnail_url = serializers.ReadOnlyField(source="thumbnail_image.url")
    image_url = serializers.ReadOnlyField(source="web_image.url")
    tags = PhotoTagSerializer(many=True, required=False)
    created_by = serializers.CharField(read_only=True)
    last_update = serializers.DateTimeField(read_only=True)

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

        if tags is not None:
            for tag in tags.split("|"):
                t, created = Tag.objects.get_or_create(name=tag)
                pt = PhotoTag(document=pic, tag=t)
                pt.save()

        return pic

    def update(self, instance, validated_data):
        tags = self.context["request"].data.get("tags", None)

        instance.tournament = validated_data.get("tournament", instance.tournament)
        instance.year = validated_data.get("year", instance.year)
        instance.caption = validated_data.get("caption", instance.caption)
        instance.photo_type = validated_data.get("photo_type", instance.photo_type)
        instance.save()

        # Delete and recreate tags.
        PhotoTag.objects.filter(document=instance).delete()
        if tags is not None:
            for tag in tags:
                t, created = Tag.objects.get_or_create(name=tag.get("name"))
                pt = PhotoTag(document=instance, tag=t)
                pt.save()

        return instance

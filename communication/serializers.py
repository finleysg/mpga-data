from communication.email import forward_contact_message
from documents.serializers import DocumentSerializer
from events.models import Event
from .models import Announcement, ContactMessage
from rest_framework import serializers


class AnnouncementSerializer(serializers.ModelSerializer):

    # event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    document = DocumentSerializer(required=False, allow_null=True)
    external_url = serializers.CharField(required=False, allow_blank=True)
    external_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Announcement
        fields = ("id", "text", "external_url", "external_name", "document", "title", "starts", "expires", )

    def create(self, validated_data):
        # doc = validated_data.pop("document")

        msg = Announcement.objects.create(
            title=validated_data.get("title"),
            text=validated_data.get("text"),
            starts=validated_data.get("starts"),
            expires=validated_data.get("expires"),
            external_url=validated_data.get("external_url", ""),
            external_name=validated_data.get("external_name", ""),
            # document=doc
        )
        msg.save()

        return msg

    def update(self, instance, validated_data):
        # doc = validated_data.pop("document")

        instance.title = validated_data.get("title", instance.title)
        instance.text = validated_data.get("text", instance.text)
        instance.starts = validated_data.get("starts", instance.starts)
        instance.expires = validated_data.get("expires", instance.expires)
        instance.external_url = validated_data.get("external_url", instance.external_url)
        instance.external_name = validated_data.get("external_name", instance.external_name)
        # instance.doc = doc

        instance.save()

        return instance


class ContactMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = ("id", "message_type", "course", "contact_name", "contact_email", "contact_phone",
                  "event", "message", "message_date", )

    def create(self, validated_data):
        message = ContactMessage.objects.create(**validated_data)
        forward_contact_message(message)
        return message

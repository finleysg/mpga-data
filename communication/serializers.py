from communication.email import forward_contact_message
from documents.serializers import DocumentSerializer
from events.models import Event
from .models import Announcement, ContactMessage
from rest_framework import serializers


class AnnouncementSerializer(serializers.ModelSerializer):

    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    document = DocumentSerializer()

    class Meta:
        model = Announcement
        fields = ("id", "text", "event", "external_url", "external_name", "document", "title", )


class ContactMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = ("id", "message_type", "course", "contact_name", "contact_email", "contact_phone",
                  "event", "message", "message_date", )

    def create(self, validated_data):
        message = ContactMessage.objects.create(**validated_data)
        forward_contact_message(message)
        return message

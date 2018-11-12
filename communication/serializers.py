from documents.serializers import DocumentSerializer
from events.models import Event
from .models import Announcement
from rest_framework import serializers


class AnnouncementSerializer(serializers.ModelSerializer):

    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    document = DocumentSerializer()

    class Meta:
        model = Announcement
        fields = ("id", "text", "event", "external_url", "external_name", "document", "title", )

from rest_framework import viewsets
from django.utils import timezone

from .models import Announcement, ContactMessage
from .serializers import AnnouncementSerializer, ContactMessageSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        today = timezone.now()
        queryset = Announcement.objects.all()
        queryset = queryset.filter(starts__lte=today, expires__gte=today)
        queryset = queryset.order_by("-id")
        return queryset


class ContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()

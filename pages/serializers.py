from .models import LandingPage
from rest_framework import serializers


class LandingPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingPage
        fields = ("id", "page_type", "title", "content", )

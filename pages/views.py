from rest_framework import viewsets

from .models import LandingPage
from .serializers import LandingPageSerializer


class LandingPageViewSet(viewsets.ModelViewSet):
    serializer_class = LandingPageSerializer
    queryset = LandingPage.objects.all()

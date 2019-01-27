from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes

from .models import SeasonSettings
from .serializers import SettingsSerializer


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class SettingsViewSet(viewsets.ModelViewSet):
    queryset = SeasonSettings.objects.all()
    serializer_class = SettingsSerializer

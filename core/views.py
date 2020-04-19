from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from .models import SeasonSettings
from .serializers import SettingsSerializer


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class SettingsViewSet(viewsets.ModelViewSet):
    queryset = SeasonSettings.objects.all()
    serializer_class = SettingsSerializer


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return Response("Email account is activated")

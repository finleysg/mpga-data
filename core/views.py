from rest_framework import viewsets

from .models import SeasonSettings
from .serializers import SettingsSerializer


class SettingsViewSet(viewsets.ModelViewSet):
    """ API endpoint to view Clubs
    """
    queryset = SeasonSettings.objects.all()
    serializer_class = SettingsSerializer


# class MemberViewSet(viewsets.ModelViewSet):
#     """ API endpoint to view a single Member
#     """
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer

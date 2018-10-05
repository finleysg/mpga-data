from rest_framework import viewsets

from .models import RegistrationGroup, Registration
from .serializers import RegistrationSerializer, RegistrationGroupSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class RegistrationGroupViewSet(viewsets.ModelViewSet):
    queryset = RegistrationGroup.objects.all()
    serializer_class = RegistrationGroupSerializer

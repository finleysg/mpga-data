from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes

from .models import Policy
from .serializers import PolicySerializer


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class PolicyViewSet(viewsets.ModelViewSet):
    serializer_class = PolicySerializer

    def get_queryset(self):
        """ Optionally filter by code
        """
        queryset = Policy.objects.all()
        policy_type = self.request.query_params.get('type', None)

        if policy_type is not None:
            queryset = queryset.filter(policy_type=policy_type)

        return queryset

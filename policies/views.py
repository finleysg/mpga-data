from rest_framework import viewsets

from .models import Policy
from .serializers import PolicySerializer


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

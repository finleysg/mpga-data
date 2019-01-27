from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes

from .models import LandingPage
from .serializers import LandingPageSerializer


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class LandingPageViewSet(viewsets.ModelViewSet):
    serializer_class = LandingPageSerializer

    def get_queryset(self):
        """ Optionally filter by year
        """
        queryset = LandingPage.objects.all()
        page = self.request.query_params.get('page', None)

        if page is not None:
            queryset = queryset.filter(page_type=page)

        return queryset

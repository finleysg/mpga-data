from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes

from .serializers import *


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class EventViewSet(viewsets.ModelViewSet):
    """ API endpoint to view Events
    """
    def get_serializer_class(self):
        name = self.request.query_params.get('name', None)
        if self.action == 'list' and name is None:
            return SimpleEventSerializer
        elif self.action == "update":
            return EventEditSerializer
        else:
            return EventDetailSerializer

    def get_queryset(self):
        """ Optionally filter by year or tournament
        """
        queryset = Event.objects.all()

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(tournament__system_name=name)

        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(start_date__year=year)

        tournament = self.request.query_params.get("tournament", None)
        if tournament is not None:
            queryset = queryset.filter(tournament=tournament)

        return queryset.order_by("start_date")


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class AwardViewSet(viewsets.ModelViewSet):
    serializer_class = AwardSerializer

    def get_queryset(self):
        """ Optionally filter by year or tournament
        """
        queryset = Award.objects.all()

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class AwardWinnerViewSet(viewsets.ModelViewSet):
    serializer_class = AwardWinnerSerializer
    queryset = AwardWinner.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class TournamentViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentSerializer

    def get_queryset(self):
        """ Optionally filter by name
        """
        queryset = Tournament.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(system_name=name)

        return queryset


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class EventLinkViewSet(viewsets.ModelViewSet):
    serializer_class = EventLinkSerializer
    queryset = EventLink.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class EventPointsViewSet(viewsets.ModelViewSet):
    serializer_class = EventPointsSerializer
    queryset = EventPoints.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class EventPolicyViewSet(viewsets.ModelViewSet):
    serializer_class = EventPolicySerializer
    queryset = EventPolicy.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class TournamentWinnerViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentWinnerSerializer

    def get_queryset(self):
        """ Optionally filter by name
        """
        queryset = TournamentWinner.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(tournament__system_name=name)

        return queryset

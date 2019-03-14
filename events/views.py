from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes

from .serializers import *


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class EventViewSet(viewsets.ModelViewSet):
    """ API endpoint to view Events
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleEventSerializer
        else:
            return EventDetailSerializer

    def get_queryset(self):
        """ Optionally filter by year or tournament
        """
        queryset = Event.objects.all()

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
    queryset = Award.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class TournamentViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentSerializer

    def get_queryset(self):
        """ Optionally filter by year
        """
        queryset = Tournament.objects.all()
        name = self.request.query_params.get('name', None)

        if name is not None:
            queryset = queryset.filter(name=name)

        return queryset


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class EventLinkViewSet(viewsets.ModelViewSet):
    serializer_class = EventLinkSerializer

    def get_queryset(self):
        queryset = EventLink.objects.all()
        tournament = self.request.query_params.get("tournament", None)

        if tournament is not None:
            queryset = queryset.filter(event__tournament__id=tournament)
            # baked in assumption: just "history-like" links, not operational links
            queryset = queryset.exclude(link_type="Tee Times").exclude(link_type="Registration")

        return queryset


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class TournamentWinnerViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentWinnerSerializer
    queryset = TournamentWinner.objects.all()

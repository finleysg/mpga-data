from datetime import datetime

from rest_framework import viewsets
from .serializers import *


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


class AwardViewSet(viewsets.ModelViewSet):
    serializer_class = AwardSerializer
    queryset = Award.objects.all()


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

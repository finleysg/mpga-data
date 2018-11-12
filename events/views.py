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
        """ Optionally filter by year
        """
        queryset = Event.objects.all()
        year = self.request.query_params.get('year', datetime.today().year)

        if year is not None:
            queryset = queryset.filter(start_date__year=year)

        return queryset.order_by("start_date")


class AwardViewSet(viewsets.ModelViewSet):
    serializer_class = AwardSerializer
    queryset = Award.objects.all()


# class AwardWinnerViewSet(viewsets.ModelViewSet):
#     serializer_class = AwardWinnerSerializer
#     queryset = AwardWinner.objects.all()


class TournamentViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()


# class TournamentWinnerViewSet(viewsets.ModelViewSet):
#     serializer_class = TournamentWinnerSerializer
#     queryset = TournamentWinner.objects.all()

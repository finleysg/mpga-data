from rest_framework import viewsets

from .models import *
from .serializers import *


class EventViewSet(viewsets.ModelViewSet):
    """ API endpoint to view Events
    """
    serializer_class = EventDetailSerializer

    def get_queryset(self):
        """ Optionally filter by year
        """
        queryset = Event.objects.all()
        year = self.request.query_params.get('year', None)

        if year is not None:
            queryset = queryset.filter(start_date__year=year)

        return queryset


class EventChairViewSet(viewsets.ModelViewSet):
    serializer_class = EventChairSerializer
    queryset = EventChair.objects.all()


class EventPointsViewSet(viewsets.ModelViewSet):
    serializer_class = EventPointsSerializer
    queryset = EventPoints.objects.all()


class EventPolicyViewSet(viewsets.ModelViewSet):
    serializer_class = EventPolicySerializer
    queryset = EventPolicy.objects.all()


class AwardViewSet(viewsets.ModelViewSet):
    serializer_class = AwardSerializer
    queryset = Award.objects.all()


class AwardWinnerViewSet(viewsets.ModelViewSet):
    serializer_class = AwardWinnerSerializer
    queryset = AwardWinner.objects.all()


class TournamentViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()


class TournamentWinnerViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentWinnerSerializer
    queryset = TournamentWinner.objects.all()

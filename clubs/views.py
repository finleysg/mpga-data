from rest_framework import viewsets
from datetime import datetime

from .serializers import *


class GolfCourseViewSet(viewsets.ModelViewSet):
    serializer_class = GolfCourseSerializer
    queryset = GolfCourse.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        queryset = Contact.objects.all()
        club = self.request.query_params.get("club", None)
        contact_type = self.request.query_params.get("type", None)
        if club is not None:
            queryset = queryset.filter(club_id=club)
        if contact_type is not None:
            queryset = queryset.filter(contact_type=contact_type)
        return queryset.order_by("last_name", "first_name", )


class ClubViewSet(viewsets.ModelViewSet):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        queryset = Membership.objects.all()
        year = self.request.query_params.get("year", datetime.today().year)
        if year is not None:
            queryset = queryset.filter(year=year)
        return queryset


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        year = self.request.query_params.get("year", None)
        if year is not None:
            queryset = queryset.filter(year=year)
        return queryset

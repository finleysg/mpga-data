from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from clubs.validation import check_club
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


class ClubContactViewSet(viewsets.ModelViewSet):
    serializer_class = ClubContactSerializer
    queryset = ClubContact.objects.all()


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


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def club_roles(request):
    roles = ClubContactRole._meta.get_field('role').choices
    return Response([r[0] for r in roles])


@api_view(("GET",))
def club_validation_messages(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    messages = check_club(club)
    return Response(messages)

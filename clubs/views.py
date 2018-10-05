from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import *


# @api_view(("GET",))
# @permission_classes((permissions.AllowAny,))
# def api_root(request):
#     return Response({
#         "courses": reverse("course-list", request=request),
#         "contacts": reverse("contact-list", request=request),
#         "clubs": reverse("club-list", request=request),
#         "memberships": reverse("membership-list", request=request),
#         "teams": reverse("team-list", request=request),
#     })


class GolfCourseViewSet(viewsets.ModelViewSet):
    serializer_class = GolfCourseDetailSerializer
    queryset = GolfCourse.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactDetailSerializer

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
    serializer_class = ClubDetailSerializer
    queryset = Club.objects.all()


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        queryset = Membership.objects.all()
        year = self.request.query_params.get("year", None)
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

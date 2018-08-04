from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import *
from .serializers import *


@api_view(("GET",))
@permission_classes((permissions.AllowAny,))
def api_root(request):
    return Response({
        "courses": reverse("course-list", request=request),
        "contacts": reverse("contact-list", request=request),
        "clubs": reverse("club-list", request=request),
        "memberships": reverse("membership-list", request=request),
        "teams": reverse("team-list", request=request),
    })


class GolfCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GolfCourseDetailSerializer
    queryset = GolfCourse.objects.all()


class GolfCourseList(generics.ListCreateAPIView):
    serializer_class = GolfCourseDetailSerializer
    queryset = GolfCourse.objects.all()


class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactDetailSerializer
    queryset = Contact.objects.all()


class ContactList(generics.ListCreateAPIView):
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


class ClubDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClubDetailSerializer
    queryset = Club.objects.all()


class ClubList(generics.ListCreateAPIView):
    serializer_class = ClubDetailSerializer
    queryset = Club.objects.all()


class MembershipDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MembershipDetailSerializer
    queryset = Membership.objects.all()


class MembershipList(generics.ListCreateAPIView):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        queryset = Membership.objects.all()
        year = self.request.query_params.get("year", None)
        if year is not None:
            queryset = queryset.filter(year=year)
        return queryset


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamDetailSerializer
    queryset = Team.objects.all()


class TeamList(generics.ListCreateAPIView):
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        year = self.request.query_params.get("year", None)
        if year is not None:
            queryset = queryset.filter(year=year)
        return queryset

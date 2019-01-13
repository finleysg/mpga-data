from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from datetime import date
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from clubs.validation import check_club
from core.models import SeasonSettings
from core.payments import stripe_charge
from .serializers import *


class GolfCourseViewSet(viewsets.ModelViewSet):
    serializer_class = GolfCourseSerializer
    queryset = GolfCourse.objects.all()


class ContactViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        is_edit = self.request.query_params.get("edit", False)
        if is_edit:
            return ContactSerializer
        else:
            return PublicContactSerializer

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
    def get_serializer_class(self):
        is_edit = self.request.query_params.get("edit", False)
        if is_edit:
            return ClubContactSerializer
        else:
            return PublicClubContactSerializer

    queryset = ClubContact.objects.all()


class ClubViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        is_edit = self.request.query_params.get("edit", False)
        if is_edit:
            return ClubSerializer
        elif self.action == 'list':
            return SimpleClubSerializer
        else:
            return PublicClubSerializer

    def get_queryset(self):
        queryset = Club.objects.all()
        is_by_user = self.request.query_params.get("user", False)
        has_team = self.request.query_params.get("has_team", False)
        if is_by_user:
            queryset = queryset.filter(club_contacts__user=self.request.user)
        if has_team:
            queryset = queryset.filter(teams__isnull=False).distinct()
        return queryset


class MembershipViewSet(viewsets.ModelViewSet):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        queryset = Membership.objects.all()
        year = self.request.query_params.get("year", None)
        if year is not None:
            queryset = queryset.filter(year=year)
        club = self.request.query_params.get("club", None)
        if club is not None:
            queryset = queryset.filter(club=club)
        return queryset


class TeamViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        is_edit = self.request.query_params.get("edit", False)
        if is_edit:
            return TeamSerializer
        elif self.action == 'list':
            return PublicTeamSerializer
        else:
            return TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        year = self.request.query_params.get("year", None)
        club = self.request.query_params.get("club", None)
        if year is not None:
            queryset = queryset.filter(year=year)
        if club is not None:
            queryset = queryset.filter(club=club)
        return queryset


class CommitteeViewSet(viewsets.ModelViewSet):
    serializer_class = CommitteeSerializer
    queryset = Committee.objects.all()


class AffiliateViewSet(viewsets.ModelViewSet):
    serializer_class = AffiliateSerializer
    queryset = Affiliate.objects.all()


class MatchPlayResultViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return MatchPlayResultListSerializer
        else:
            return MatchPlayResultSerializer

    def get_queryset(self):
        queryset = MatchPlayResult.objects.all()
        year = self.request.query_params.get("year", None)
        if year is not None:
            queryset = queryset.filter(match_date__year=year)
        return queryset


@api_view(('GET',))
def club_roles(request):
    roles = ClubContactRole._meta.get_field('role').choices
    return Response([r[0] for r in roles])


@api_view(("GET",))
def club_validation_messages(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    messages = check_club(club)
    return Response(messages)


@api_view(("GET",))
def is_club_contact(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    email = request.query_params.get("email", None)
    if email:
        try:
            club.club_contacts.get(contact__email=email)
            return Response(True)
        except ObjectDoesNotExist:
            return Response(False)
    else:
        return Response(False)

#
# @api_view(("GET",))
# @permission_classes((permissions.IsAuthenticated,))
# def get_club_for_user(request):
#     clubs = list(Club.objects.filter(club_contact__user=request.user))
#     serializer = ClubSerializer(clubs, many=True, context={"request": request})
#     return Response(serializer.data)


@api_view(("POST",))
@permission_classes((permissions.IsAuthenticated,))
def pay_club_membership(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    year = request.data.get("year", None)
    token = request.data.get("token", None)

    # TODO: can this be truly transactional?
    # process payment via Stripe
    config = SeasonSettings.objects.current_settings()
    description = "{} membership dues for {}".format(year, club.name)
    charge = stripe_charge(request.user, token, description, int(100 * config.membership_dues))

    # create our membership object
    mem = Membership(year=year, club=club, payment_date=date.today(), payment_type="OL", payment_code=charge.id)
    mem.save()

    serializer = MembershipSerializer(mem, context={"request": request})
    return Response(serializer.data)

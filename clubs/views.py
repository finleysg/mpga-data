import logging

import stripe
from django.shortcuts import get_object_or_404
from datetime import date

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from communication.email import send_dues_confirmation
from core.models import SeasonSettings
from .serializers import *

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET
logger = logging.getLogger(__name__)

def current_season():
    today = date.today()
    return today.year


def get_payment_intent(amount_due, club, user_email):
    return stripe.PaymentIntent.create(
        amount=amount_due,
        currency='usd',
        automatic_payment_methods={"enabled": True},
        description='Club dues for ' + club.name,
        metadata={
            'club_id': str(club.id),
            'club_name': club.name,
            'user_email': user_email,
        },
        receipt_email=user_email,
    )


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class GolfCourseViewSet(viewsets.ModelViewSet):
    serializer_class = GolfCourseSerializer
    queryset = GolfCourse.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class ClubRoleViewSet(viewsets.ModelViewSet):
    serializer_class = ClubRoleSerializer
    queryset = ClubRole.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class ContactViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        # is_edit = self.request.query_params.get("edit", False)
        if self.request.user.is_authenticated:
            return ContactSerializer
        else:
            return PublicContactSerializer

    def get_queryset(self):
        queryset = Contact.objects.all()
        club = self.request.query_params.get("club", None)
        email = self.request.query_params.get("email", None)
        pattern = self.request.query_params.get("pattern", None)
        if club is not None:
            queryset = queryset.filter(club_id=club)
        if email is not None:
            queryset = queryset.filter(email=email)
        if pattern is not None:
            queryset = queryset.filter(last_name__icontains=pattern) | queryset.filter(first_name__icontains=pattern)
        return queryset.order_by("last_name", "first_name", )


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class ClubContactViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        is_edit = self.request.query_params.get("edit", False)
        if is_edit or self.request.user.is_authenticated:
            return ClubContactSerializer
        else:
            return PublicClubContactSerializer

    queryset = ClubContact.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class ClubViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        system_name = self.request.query_params.get("name", None)
        if self.action == 'list':
            if system_name is not None:
                if self.request.user.is_authenticated:
                    return ClubSerializer
                else:
                    return PublicClubSerializer
            else:
                return SimpleClubSerializer
        else:
            if self.request.user.is_authenticated:
                return ClubSerializer
            else:
                return PublicClubSerializer

    def get_queryset(self):
        queryset = Club.objects.all()
        is_by_user = self.request.query_params.get("user", False)
        has_team = self.request.query_params.get("has_team", False)
        system_name = self.request.query_params.get("name", False)
        pattern = self.request.query_params.get("pattern", False)
        if is_by_user:
            queryset = queryset.filter(club_contacts__user=self.request.user)
        if has_team:
            queryset = queryset.filter(teams__isnull=False).distinct()
        if system_name:
            queryset = queryset.filter(system_name=system_name)
        if pattern:
            queryset = queryset.filter(name__icontains=pattern)
        return queryset


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
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


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class TeamViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        is_edit = self.request.query_params.get("edit", False)
        if is_edit:
            return TeamSerializer
        elif self.action == 'list' and self.request.user.is_authenticated:
            return TeamListSerializer
        else:
            return PublicTeamListSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        year = self.request.query_params.get("year", None)
        club = self.request.query_params.get("club", None)
        if year is not None:
            queryset = queryset.filter(year=year)
        if club is not None:
            queryset = queryset.filter(club=club)
        return queryset.order_by("is_senior", "group_name", "club__name", )


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class CommitteeViewSet(viewsets.ModelViewSet):
    serializer_class = CommitteeSerializer

    def get_queryset(self):
        queryset = Committee.objects.all()
        return queryset.order_by("contact__last_name",)


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
class AffiliateViewSet(viewsets.ModelViewSet):
    serializer_class = AffiliateSerializer
    queryset = Affiliate.objects.all()


@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
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
@permission_classes((permissions.IsAuthenticated,))
def contact_roles(request):
    email = request.query_params.get("email", None)
    if email is None:
        return Response([])

    ec = Committee.objects.filter(contact__email=email).values("id")
    cc = ClubContact.objects.filter(contact__email=email).values("club__system_name")
    data = {
        "committee": list(ec),
        "club": list(cc),
    }
    return Response(data=data)


@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
def club_roles(request):
    pattern = request.query_params.get("pattern", None)
    if pattern is not None:
        roles = ClubContactRole._meta.get_field('role').choices
        return Response([r[0] for r in roles if pattern.lower() in r[0].lower()])

    roles = ClubContactRole._meta.get_field('role').choices
    return Response([r[0] for r in roles])

## PAYMENT HANDLING ##

@api_view(("POST", ))
@permission_classes((permissions.AllowAny,))
def create_payment_intent(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    user_email = request.data.get("email", None)
    config = SeasonSettings.objects.current_settings()

    intent = get_payment_intent(int(100 * config.membership_dues), club, user_email)

    return Response(intent, status=200)


# This is a webhook registered with Stripe
@csrf_exempt
@api_view(("POST",))
@permission_classes((permissions.AllowAny,))
def club_dues_complete(request):
    try:
        # Verify and construct the Stripe event
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

        logger.debug(f"Received webhook: {payload} with signature {sig_header}, validated with secret {webhook_secret}")

        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)

        # Handle the event
        if event is None:
            return Response(status=400)
        elif event.type == 'payment_intent.payment_failed':
            payment_intent = event.data.object
            error = payment_intent.last_payment_error
            logger.error(f"Payment failure: email={payment_intent.metadata.get('user_email')}, intent_id={payment_intent.id}, error={error.message}")
        elif event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            handle_club_dues_complete(payment_intent)
        else:
            logger.debug("Unhandled event: " + event.type)

        return Response(status=204)

    except stripe.error.SignatureVerificationError as ve:
        logger.error("Invalid signature in webhook")
        logger.error(ve)
        return Response(status=400)
    except Exception as e:
        logger.error(e)
        return Response(status=400)


def handle_club_dues_complete(payment_intent):
    club_id = payment_intent.metadata.get("club_id")
    club = get_object_or_404(Club, pk=club_id)
    year = current_season()

    user_name = payment_intent.metadata.get("user_name")
    logger.info(f"Completing online payment for club={club.name}, user_name={user_name}, season={year}")

    # create our membership object
    mem = Membership(year=year, club=club, payment_date=date.today(), payment_type="OL", payment_code=payment_intent.id)
    mem.save()

    try:
        send_dues_confirmation(year, club)
    except Exception as exc:
        logger.error("Failed to send membership confirmation")
        logger.error(exc)

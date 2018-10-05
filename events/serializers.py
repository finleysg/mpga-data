from rest_framework import serializers

from clubs.serializers import ContactSerializer, GolfCourseSerializer
from documents.serializers import DocumentSerializer
from policies.serializers import PolicySerializer
from register.serializers import RegistrationSerializer
from .models import *


class AwardWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardWinner
        fields = ("id", "year", "award", "winner", "notes", )


class TournamentWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentWinner
        fields = ("id", "year", "tournament", "location", "winner", "winner_club", "co_winner", "co_winner_club",
                  "flight_or_division", "score", "is_net", "notes", )


class AwardSerializer(serializers.ModelSerializer):
    winners = AwardWinnerSerializer(many=True)

    class Meta:
        model = Award
        fields = ("id", "name", "description", "winners", )


class TournamentSerializer(serializers.ModelSerializer):
    winners = TournamentWinnerSerializer(many=True)

    class Meta:
        model = Tournament
        fields = ("id", "name", "description", "winners", )


class EventChairSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    chair = ContactSerializer()

    class Meta:
        model = EventChair
        fields = ("id", "event", "chair", )


class EventPointsSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EventPoints
        fields = ("id", "event", "place", "points", "ordinal_place", )


class EventPolicySerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    policy = PolicySerializer()

    class Meta:
        model = EventPolicy
        fields = ("id", "event", "policy", "order", )


class EventDetailSerializer(serializers.ModelSerializer):

    location = GolfCourseSerializer()
    tournament = TournamentSerializer()
    documents = DocumentSerializer(many=True)
    registrations = RegistrationSerializer(many=True)
    policies = EventPolicySerializer(many=True)
    chairs = EventChairSerializer(many=True)
    player_points = EventPointsSerializer(many=True)

    class Meta:
        model = Event
        fields = ("id", "location", "name", "description", "rounds", "event_fee",
                  "minimum_signup_group_size", "maximum_signup_group_size", "tournament",
                  "registration_url", "registration_type", "portal_url", "notes", "event_type", "alt_event_fee",
                  "start_date", "registration_start", "registration_end", "early_registration_end",
                  "registration_maximum", "documents", "registrations", "policies", "chairs", "player_points", )

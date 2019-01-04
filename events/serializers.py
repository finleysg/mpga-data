from rest_framework import serializers

from clubs.serializers import ContactSerializer, GolfCourseSerializer
from policies.serializers import PolicySerializer
from .models import *


class AwardWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardWinner
        fields = ("id", "year", "award", "winner", "notes", )


class TournamentWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentWinner
        fields = ("id", "year", "tournament", "location", "winner", "winner_club", "co_winner", "co_winner_club",
                  "flight_or_division", "score", "is_net", "is_match", "notes", )


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


class EventDivisionSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EventDivision
        fields = ("id", "event", "division", )


class EventFeeSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EventFee
        fields = ("id", "event", "fee_type", "amount", "ec_only", )


class EventLinkSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EventLink
        fields = ("id", "event", "link_type", "title", "url", )


class EventDetailSerializer(serializers.ModelSerializer):

    location = GolfCourseSerializer()
    policies = EventPolicySerializer(many=True)
    chairs = EventChairSerializer(many=True)
    player_points = EventPointsSerializer(many=True)
    divisions = EventDivisionSerializer(many=True)
    links = EventLinkSerializer(many=True)
    fees = EventFeeSerializer(many=True)

    class Meta:
        model = Event
        fields = ("id", "location", "name", "description", "rounds", "short_name",
                  "minimum_signup_group_size", "maximum_signup_group_size", "tournament",
                  "registration_type", "notes", "event_type",
                  "start_date", "registration_start", "registration_end", "early_registration_end",
                  "registration_maximum", "policies", "chairs", "player_points",
                  "divisions", "links", "fees", )


class SimpleEventSerializer(serializers.ModelSerializer):

    location = GolfCourseSerializer()
    links = EventLinkSerializer(many=True)

    class Meta:
        model = Event
        fields = ("id", "location", "name", "description", "rounds", "short_name",
                  "registration_type", "event_type", "registration_maximum", "links",
                  "start_date", "registration_start", "registration_end", "early_registration_end", )

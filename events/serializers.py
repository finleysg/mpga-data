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
    winners = AwardWinnerSerializer(many=True, read_only=True)

    class Meta:
        model = Award
        fields = ("id", "name", "description", "winners", )


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ("id", "name", "system_name", "description", )


class EventChairSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    chair = ContactSerializer()

    class Meta:
        model = EventChair
        fields = ("id", "event", "chair", )


class EventPointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventPoints
        fields = ("id", "event", "place", "points", "ordinal_place", )


class EventPolicySerializer(serializers.ModelSerializer):
    policy = PolicySerializer()

    class Meta:
        model = EventPolicy
        fields = ("id", "event", "policy", "order", )

    def create(self, validated_data):
        policy = validated_data.pop("policy")

        if policy.get("id", 0) == 0:
            policy["id"] = None  # mysql won't accept 0
            this_policy = Policy.objects.create(**policy)
        else:
            this_policy = policy

        ep = EventPolicy.objects.create(
            policy=this_policy,
            event=validated_data.get("event", 0),
            order=validated_data.get("order", 0)
        )
        ep.save()

        return ep

    def update(self, instance, validated_data):
        policy_data = validated_data.pop("policy")

        policy = instance.policy
        policy.policy_type = policy_data.get("policy_type", policy.policy_type)
        policy.name = policy_data.get("name", policy.name)
        policy.title = policy_data.get("title", policy.title)
        policy.description = policy_data.get("description", policy.description)
        policy.save()

        instance.order = validated_data.get("order", instance.order)
        instance.save()

        return instance


class EventLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventLink
        fields = ("id", "event", "link_type", "title", "url", )


class EventDetailSerializer(serializers.ModelSerializer):

    location = GolfCourseSerializer()
    tournament = TournamentSerializer()
    policies = EventPolicySerializer(many=True)
    chairs = EventChairSerializer(many=True)
    player_points = EventPointsSerializer(many=True)
    links = EventLinkSerializer(many=True)

    class Meta:
        model = Event
        fields = ("id", "location", "tournament", "name", "description", "rounds", "tournament",
                  "notes", "event_type", "start_date", "registration_start", "registration_end",
                  "early_registration_end", "policies", "chairs", "player_points", "links", )


class SimpleEventSerializer(serializers.ModelSerializer):

    location = GolfCourseSerializer()
    tournament = TournamentSerializer()
    links = EventLinkSerializer(many=True)

    class Meta:
        model = Event
        fields = ("id", "location", "tournament", "name", "description", "rounds", "event_type", "links",
                  "start_date", "registration_start", "registration_end", "early_registration_end", )


class EventEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ("id", "location", "tournament", "name", "description", "rounds", "tournament", "notes",
                  "event_type", "start_date", "registration_start", "registration_end", "early_registration_end", )

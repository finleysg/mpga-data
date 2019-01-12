from django.contrib.auth.models import User, Group

from .models import SeasonSettings
from rest_framework import serializers


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeasonSettings
        fields = ("event_calendar_year", "match_play_year", "member_club_year", "match_play_finalized",
                  "membership_dues", "raven_dsn", "stripe_public_key", "match_play_divisions", "match_play_groups", )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email",
                  "is_authenticated", "is_staff", "is_active", "password", "groups", )
        read_only_fields = ("id", "is_authenticated", "is_staff", "is_active", )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user

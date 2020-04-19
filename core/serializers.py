import random
import string
from django.contrib.auth.models import User, Group

from clubs.models import Contact
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


class UserDetailSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email",
                  "is_authenticated", "is_staff", "is_active", "groups", )
        read_only_fields = ("id", "is_authenticated", "is_staff", "is_active", )

    def update(self, instance, validated_data):
        contact = Contact.objects.get(email=instance.email)

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        contact.email = validated_data.get("email", instance.email)
        contact.first_name = validated_data.get("first_name", instance.first_name)
        contact.last_name = validated_data.get("last_name", instance.last_name)
        contact.save()

        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", )

    def create(self, validated_data):
        uname = "".join([random.choice(string.ascii_lowercase) for n in range(24)])
        user = User.objects.create_user(
            username=uname,
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=False,
        )

        Contact.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email, send_email=True)

        return user

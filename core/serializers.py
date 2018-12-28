from django.contrib.auth.models import User, Group

from clubs.serializers import ClubSerializer, ContactSerializer
from .models import Member, SeasonSettings
from rest_framework import serializers


class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeasonSettings
        fields = ("event_calendar_year", "match_play_year", "member_club_year", )


class MemberSerializer(serializers.ModelSerializer):
    home_club = ClubSerializer()
    contact = ContactSerializer()

    class Meta:
        model = Member
        fields = ("id", "home_club", "contact", )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    member = MemberSerializer()
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "member",
                  "is_authenticated", "is_staff", "is_active", "password", "groups", )
        read_only_fields = ("id", "is_authenticated", "is_staff", "is_active", )

    def update(self, instance, validated_data):
        member_data = validated_data.pop("member")

        member = instance.member

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        member.home_club = member_data.get("home_club", member.home_club)
        member.contact = member_data.get("contact", member.contact)
        member.save()

        return instance

    def create(self, validated_data):
        member_data = validated_data.pop("member")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        Member.objects.create(
            home_club=member_data.get("home_club", ""),
            contact=member_data.get("contact", ""),
            user=user
        )
        return user


class SimpleMemberSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Member
        fields = ("id", "first_name", "last_name", "email", )

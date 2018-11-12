from .models import *
from rest_framework import serializers


class GolfCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = GolfCourse
        fields = ("id", "name", "address_txt", "city", "state", "zip", "website", "email", "phone", "notes", )


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "contact_type", "primary_phone", "alternate_phone", "email",
                  "address_txt", "city", "state", "zip", "notes", )


class ClubContactRoleSerializer(serializers.ModelSerializer):
    club_contact = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClubContactRole
        fields = ("id", "club_contact", "role", )


class ClubContactSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(read_only=True)
    contact = ContactSerializer()
    roles = ClubContactRoleSerializer(many=True)

    class Meta:
        model = ClubContact
        fields = ("id", "club", "contact", "is_primary", "use_for_mailings", "roles", )


class ClubSerializer(serializers.ModelSerializer):

    golf_course = GolfCourseSerializer()
    club_contacts = ClubContactSerializer(many=True)

    class Meta:
        model = Club
        fields = ("id", "name", "golf_course", "website", "type_2", "notes", "size", "club_contacts", )


class MembershipSerializer(serializers.ModelSerializer):

    # club = serializers.PrimaryKeyRelatedField(read_only=True)
    club = ClubSerializer()

    class Meta:
        model = Membership
        fields = ("id", "year", "club", "payment_date", "payment_type", "payment_code", "create_date", "notes", )


class TeamSerializer(serializers.ModelSerializer):

    # club = serializers.PrimaryKeyRelatedField(read_only=True)
    club = ClubSerializer()
    captain = ContactSerializer()
    co_captain = ContactSerializer()

    class Meta:
        model = Team
        fields = ("id", "year", "club", "captain", "co_captain", "group_name", "is_senior", "notes", )

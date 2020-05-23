from .models import *
from rest_framework import serializers


class GolfCourseSerializer(serializers.ModelSerializer):

    logo_url = serializers.ReadOnlyField(source="web_logo.url")

    class Meta:
        model = GolfCourse
        fields = ("id", "name", "address_txt", "city", "state", "zip", "website", "email", "phone",
                  "logo_url", "notes", )


class SimpleGolfCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = GolfCourse
        fields = ("id", "name", "city", )


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "primary_phone", "alternate_phone", "email",
                  "send_email", "home_club", "address_txt", "city", "state", "zip", "notes", )


class PublicContactSerializer(serializers.ModelSerializer):

    primary_phone = serializers.CharField(source="public_primary_phone")
    alternate_phone = serializers.CharField(source="public_alternate_phone")
    email = serializers.CharField(source="public_email")

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "primary_phone", "alternate_phone", "home_club",
                  "email", "city", "notes", )


class ClubContactRoleSerializer(serializers.ModelSerializer):
    club_contact = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClubContactRole
        fields = ("id", "club_contact", "role", )


class ClubContactSerializer(serializers.ModelSerializer):
    # club = serializers.PrimaryKeyRelatedField(read_only=True)
    contact = ContactSerializer()
    roles = ClubContactRoleSerializer(many=True)

    class Meta:
        model = ClubContact
        fields = ("id", "club", "contact", "is_primary", "use_for_mailings", "roles", "notes", )

    def create(self, validated_data):
        roles = validated_data.pop("roles")
        contact = validated_data.pop("contact")

        if contact.get("id", 0) == 0:
            contact["id"] = None  # mysql won't accept 0
            cc_contact = Contact.objects.create(**contact)
        else:
            cc_contact = contact

        cc = ClubContact.objects.create(
            club=validated_data.get("club", None),
            contact=cc_contact,
            is_primary=validated_data.get("is_primary", False),
            use_for_mailings=validated_data.get("use_for_mailings", False),
            notes=validated_data.get("notes", None)
        )

        for r in roles:
            r["id"] = None  # mysql won't accept 0
            role = ClubContactRole.objects.create(club_contact=cc, **r)
            cc.roles.add(role)

        cc.save()

        return cc

    def update(self, instance, validated_data):
        roles = validated_data.pop("roles")
        contact_data = validated_data.pop("contact")

        # Delete and recreate roles.
        ClubContactRole.objects.filter(club_contact=instance).delete()
        for r in roles:
            r["id"] = None  # mysql won't accept 0
            role = ClubContactRole.objects.create(club_contact=instance, **r)
            instance.roles.add(role)

        contact = instance.contact
        contact.first_name = contact_data.get("first_name", contact.first_name)
        contact.last_name = contact_data.get("last_name", contact.last_name)
        contact.primary_phone = contact_data.get("primary_phone", contact.primary_phone)
        contact.alternate_phone = contact_data.get("alternate_phone", contact.alternate_phone)
        contact.email = contact_data.get("email", contact.email)
        contact.send_email = contact_data.get("send_email", contact.send_email)
        contact.home_club = contact_data.get("home_club", contact.home_club)
        contact.address_txt = contact_data.get("address_txt", contact.address_txt)
        contact.city = contact_data.get("city", contact.city)
        contact.state = contact_data.get("state", contact.state)
        contact.zip = contact_data.get("zip", contact.zip)
        contact.notes = contact_data.get("notes", contact.notes)
        contact.save()

        instance.is_primary = validated_data.get("is_primary", instance.is_primary)
        instance.use_for_mailings = validated_data.get("use_for_mailings", instance.use_for_mailings)
        instance.notes = validated_data.get("notes", instance.notes)

        instance.save()

        return instance


class PublicClubContactSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(read_only=True)
    contact = PublicContactSerializer()
    roles = ClubContactRoleSerializer(many=True)

    class Meta:
        model = ClubContact
        fields = ("id", "club", "contact", "is_primary", "use_for_mailings", "roles", "notes", )


class ClubSerializer(serializers.ModelSerializer):

    golf_course = GolfCourseSerializer(read_only=True)
    club_contacts = ClubContactSerializer(many=True)

    class Meta:
        model = Club
        fields = ("id", "name", "system_name", "golf_course", "website", "notes", "size", "club_contacts", )

    def update(self, instance, validated_data):

        # only update fields on the model -- club contacts managed separately,
        # golf course is read only and changeable only in the admin site
        instance.name = validated_data.get("name", instance.name)
        instance.website = validated_data.get("website", instance.website)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.size = validated_data.get("size", instance.size)

        instance.save()

        return instance


class PublicClubSerializer(serializers.ModelSerializer):

    golf_course = GolfCourseSerializer()
    club_contacts = PublicClubContactSerializer(many=True)

    class Meta:
        model = Club
        fields = ("id", "name", "system_name", "golf_course", "website", "notes", "size", "club_contacts", )


class SimpleClubSerializer(serializers.ModelSerializer):

    golf_course = SimpleGolfCourseSerializer()

    class Meta:
        model = Club
        fields = ("id", "name", "system_name", "golf_course", "website", "notes", "size", )


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ("id", "year", "club", "payment_date", "payment_type", "payment_code", "notes", )


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "year", "club", "group_name", "is_senior", "notes", )


class TeamListSerializer(serializers.ModelSerializer):

    club = ClubSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "year", "club", "group_name", "is_senior", "notes", )


class PublicTeamListSerializer(serializers.ModelSerializer):

    club = PublicClubSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "year", "club", "group_name", "is_senior", "notes", )


class MatchPlayResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchPlayResult
        fields = ("id", "group_name", "match_date", "home_team", "away_team", "home_team_score", "away_team_score",
                  "entered_by", "forfeit", "notes", )


class MatchPlayResultListSerializer(serializers.ModelSerializer):

    home_team_name = serializers.CharField(source="home_team.name")
    away_team_name = serializers.CharField(source="away_team.name")

    class Meta:
        model = MatchPlayResult
        fields = ("id", "group_name", "match_date", "home_team", "away_team", "home_team_score", "away_team_score",
                  "entered_by", "forfeit", "notes", "home_team_name", "away_team_name", )


class CommitteeSerializer(serializers.ModelSerializer):

    contact = ContactSerializer()
    home_club_name = serializers.CharField(source="home_club.name", read_only=True)

    class Meta:
        model = Committee
        fields = ("id", "role", "home_club", "home_club_name", "contact", )

    def create(self, validated_data):
        contact = validated_data.pop("contact")

        if contact.get("id", 0) == 0:
            contact["id"] = None  # mysql won't accept 0
            cc_contact = Contact.objects.create(**contact)
        else:
            cc_contact = contact

        ec = Committee.objects.create(
            role=validated_data.get("role", None),
            home_club=validated_data.get("home_club", None),
            contact=cc_contact,
        )

        ec.save()

        return ec

    def update(self, instance, validated_data):
        contact_data = validated_data.pop("contact")

        contact = instance.contact
        contact.first_name = contact_data.get("first_name", contact.first_name)
        contact.last_name = contact_data.get("last_name", contact.last_name)
        contact.primary_phone = contact_data.get("primary_phone", contact.primary_phone)
        contact.alternate_phone = contact_data.get("alternate_phone", contact.alternate_phone)
        contact.email = contact_data.get("email", contact.email)
        contact.address_txt = contact_data.get("address_txt", contact.address_txt)
        contact.city = contact_data.get("city", contact.city)
        contact.state = contact_data.get("state", contact.state)
        contact.zip = contact_data.get("zip", contact.zip)
        contact.notes = contact_data.get("notes", contact.notes)
        contact.save()

        instance.role = validated_data.get("role", instance.role)
        instance.home_club = validated_data.get("home_club", instance.home_club)

        instance.save()

        return instance


class AffiliateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliate
        fields = ("id", "organization", "website", "notes", )

from .models import *
from rest_framework import serializers


class GolfCourseSerializer(serializers.ModelSerializer):

    logo_url = serializers.ReadOnlyField(source="web_logo.url")

    class Meta:
        model = GolfCourse
        fields = ("id", "name", "address_txt", "city", "state", "zip", "website", "email", "phone",
                  "logo_url", "notes", )


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "contact_type", "primary_phone", "alternate_phone", "email",
                  "address_txt", "city", "state", "zip", "notes", )


class PublicContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "contact_type", "public_phone", "public_email",
                  "public_address", "notes", )


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
        fields = ("id", "club", "contact", "is_primary", "use_for_mailings", "roles", "notes", )

    def create(self, validated_data):
        roles = validated_data.pop("roles")
        contact = validated_data.pop("contact")
        cc = ClubContact.objects.create(**validated_data)

        if contact["id"] == 0:
            contact["id"] = None  # mysql won't accept 0
            cc.contact = Contact.create(club_contact=cc, **contact)
        else:
            cc.contact = contact

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
        contact.contact_type = contact_data.get("contact_type", contact.contact_type)
        contact.primary_phone = contact_data.get("primary_phone", contact.primary_phone)
        contact.alternate_phone = contact_data.get("alternate_phone", contact.alternate_phone)
        contact.email = contact_data.get("email", contact.email)
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

    golf_course = GolfCourseSerializer()
    club_contacts = ClubContactSerializer(many=True)

    class Meta:
        model = Club
        fields = ("id", "name", "golf_course", "website", "type_2", "notes", "size", "club_contacts", )

    def update(self, instance, validated_data):

        # only update fields on the model -- club contacts managed separately,
        # golf course is read only and changeable only in the admin site
        instance.name = validated_data.get("name", instance.name)
        instance.website = validated_data.get("website", instance.website)
        instance.type_2 = validated_data.get("type_2", instance.type_2)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.size = validated_data.get("size", instance.size)

        instance.save()

        return instance


class PublicClubSerializer(serializers.ModelSerializer):

    golf_course = GolfCourseSerializer()
    club_contacts = PublicClubContactSerializer(many=True)

    class Meta:
        model = Club
        fields = ("id", "name", "golf_course", "website", "type_2", "notes", "size", "club_contacts", )


class MembershipSerializer(serializers.ModelSerializer):

    club = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Membership
        fields = ("id", "year", "club", "payment_date", "payment_type", "payment_code", "create_date", "notes", )


class TeamSerializer(serializers.ModelSerializer):

    club = PublicClubSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "year", "club", "group_name", "is_senior", "notes", )


class CommitteeSerializer(serializers.ModelSerializer):

    home_club = serializers.CharField(source="home_club.name")
    contact = PublicContactSerializer()

    class Meta:
        model = Committee
        fields = ("id", "role", "home_club", "contact", )


class AffiliateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliate
        fields = ("id", "organization", "website", "notes", )

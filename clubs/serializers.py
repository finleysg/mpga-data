from .models import *
from rest_framework import serializers


class GolfCourseDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = GolfCourse
        fields = ("id", "name", "address_txt", "city", "state", "zip", "website", "email", "phone", "notes", )

    def create(self, validated_data):
        name = validated_data.pop("name")
        address_txt = validated_data.pop("address_txt", None)
        city = validated_data.get("city", None)
        state = validated_data.get("state", None)
        zip = validated_data.get("zip", None)
        website = validated_data.get("website", None)
        email = validated_data.get("email", None)
        phone = validated_data.get("phone", None)
        notes = validated_data.get("notes", None)

        gc = GolfCourse(name=name, address_txt=address_txt, city=city, state=state, zip=zip, website=website,
                         email=email, phone=phone, notes=notes)
        gc.save()
        return gc

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address_txt = validated_data.get("address_txt", instance.address_txt)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.zip = validated_data.get("zip", instance.zip)
        instance.website = validated_data.get("website", instance.website)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()

        return instance


class GolfCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = GolfCourse
        fields = ("id", "name", "address_txt", "city", "state", "zip", "website", "email", "phone", "notes", )


class ContactDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "contact_type", "primary_phone", "alternate_phone", "email",
                  "address_txt", "city", "state", "zip", "notes", )

    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        contact_type = validated_data.pop("contact_type")
        primary_phone = validated_data.get("primary_phone", None)
        alternate_phone = validated_data.get("alternate_phone", None)
        email = validated_data.get("email", None)
        address_txt = validated_data.pop("address_txt", None)
        city = validated_data.get("city", None)
        state = validated_data.get("state", None)
        zip = validated_data.get("zip", None)
        notes = validated_data.get("notes", None)

        contact = Contact(first_name=first_name, last_name=last_name, contact_type=contact_type,
                          primary_phone=primary_phone, alternate_phone=alternate_phone, email=email,
                          address_txt=address_txt, city=city, state=state, zip=zip, notes=notes)
        contact.save()
        return contact

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.contact_type = validated_data.get("contact_type", instance.contact_type)
        instance.primary_phone = validated_data.get("primary_phone", instance.primary_phone)
        instance.alternate_phone = validated_data.get("alternate_phone", instance.alternate_phone)
        instance.email = validated_data.get("email", instance.email)
        instance.address_txt = validated_data.get("address_txt", instance.address_txt)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.zip = validated_data.get("zip", instance.zip)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()

        return instance


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ("id", "first_name", "last_name", "contact_type", "primary_phone", "alternate_phone", "email",
                  "address_txt", "city", "state", "zip", "notes", )


class ClubSerializer(serializers.ModelSerializer):

    golf_course = GolfCourseSerializer()

    class Meta:
        model = Club
        fields = ("id", "name", "website", "type_2", "notes", "golf_course", )


class MembershipDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ("id", "year", "club_id", "payment_date", "payment_type", "payment_code", "create_date", "notes", )

    def create(self, validated_data):
        year = validated_data.pop("year")
        club_id = validated_data.pop("club_id")
        payment_date = validated_data.pop("payment_date")
        payment_type = validated_data.pop("payment_type")
        payment_code = validated_data.get("payment_cd", None)
        create_date = validated_data.get("create_date", None)
        notes = validated_data.get("notes", None)

        membership = Membership(year=year, club_id=club_id, payment_date=payment_date, payment_type=payment_type,
                                payment_code=payment_code, create_date=create_date, notes=notes)
        membership.save()
        return membership

    def update(self, instance, validated_data):
        instance.year = validated_data.get("year", instance.year)
        instance.club_id = validated_data.get("club_id", instance.club_id)
        instance.payment_date = validated_data.get("payment_date", instance.payment_date)
        instance.payment_type = validated_data.get("payment_type", instance.payment_type)
        instance.payment_code = validated_data.get("payment_code", instance.payment_code)
        instance.create_date = validated_data.get("create_date", instance.create_date)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()

        return instance


class MembershipSerializer(serializers.ModelSerializer):

    club = ClubSerializer()

    class Meta:
        model = Membership
        fields = ("id", "year", "club", "payment_date", "payment_type", "payment_code", "create_date", "notes", )


class TeamDetailSerializer(serializers.ModelSerializer):

    contact = ContactSerializer()

    class Meta:
        model = Team
        fields = ("id", "year", "club_id", "contact", "group_name", "is_senior", "notes", )

    def create(self, validated_data):
        contact = validated_data.get("contact", None)
        year = validated_data.pop("year")
        club_id = validated_data.pop("club_id")
        contact_id = contact.id if contact is not None else None
        group_name = validated_data.pop("group_name")
        is_senior = validated_data.get("is_senior", False)
        notes = validated_data.get("notes", None)

        team = Team(year=year, club_id=club_id, contact_id=contact_id, group_name=group_name, is_senior=is_senior, notes=notes)
        team.save()
        return team

    def update(self, instance, validated_data):
        instance.year = validated_data.get("year", instance.year)
        instance.club_id = validated_data.get("club_id", instance.club_id)
        instance.contact_id = validated_data.get("contact_id", instance.contact_id)
        instance.group_name = validated_data.get("group_name", instance.group_name)
        instance.is_senior = validated_data.get("is_senior", instance.is_senior)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()

        return instance


class TeamSerializer(serializers.ModelSerializer):

    club = ClubSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "year", "club", "contact", "group_name", "is_senior", )


class ClubContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClubContact
        fields = ("id", "club_id", "contact_id", "role", "is_primary", "use_for_mailings", )


class ClubDetailSerializer(serializers.ModelSerializer):

    golf_course = GolfCourseSerializer()
    contacts = ContactSerializer(many=True, read_only=True)
    memberships = MembershipDetailSerializer(many=True, read_only=True)
    teams = TeamDetailSerializer(many=True, read_only=True)
    club_to_contact = ClubContactSerializer(many=True)

    class Meta:
        model = Club
        fields = ("id", "name", "golf_course", "website", "type_2", "notes",
                  "contacts", "club_to_contact", "memberships", "teams", )

    def create(self, validated_data):
        name = validated_data.pop("name")
        course = validated_data.get("golf_course", None)
        website = validated_data.get("website", None)
        type_2 = validated_data.get("type_2", False)
        notes = validated_data.get("notes", None)

        club = Club(name=name, golf_course=course, website=website, type_2=type_2, notes=notes)
        club.save()
        return club

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address_txt = validated_data.get("address_txt", instance.address_txt)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.zip = validated_data.get("zip", instance.zip)
        instance.website = validated_data.get("website", instance.website)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.save()

        return instance

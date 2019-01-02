from rest_framework import serializers

from .models import RegistrationGroup, Registration, Participant


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
        fields = ("id", "home_club", "last_name", "first_name", "email", "ghin", )


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ("id", "event", "registration_group", "is_event_fee_paid", "event_fee", "participant")
        order_by = ("event", "registration_group", )


class RegistrationGroupSerializer(serializers.ModelSerializer):

    registrations = RegistrationSerializer(many=True)

    class Meta:
        model = RegistrationGroup
        fields = ("id", "event", "registered_by", "notes", "payment_confirmation_code", "division",
                  "payment_confirmation_timestamp", "payment_amount", "card_verification_token", "registrations", )

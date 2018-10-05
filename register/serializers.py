from rest_framework import serializers

from core.models import Member
from core.serializers import SimpleMemberSerializer
from .models import RegistrationGroup, Registration


class RegistrationSerializer(serializers.ModelSerializer):
    member = SimpleMemberSerializer()

    class Meta:
        model = Registration
        fields = ("id", "event", "registration_group", "is_event_fee_paid", "event_fee", "member")
        order_by = ("event", "registration_group", )

    def update(self, instance, validated_data):
        member = instance.member
        if member is None:
            member_data = validated_data.pop('member')
            member = Member.objects.get(pk=member_data['id'])

        instance.member = member
        instance.registration_group = validated_data.get('registration_group', instance.registration_group)
        instance.event_fee = validated_data.get('event_fee', instance.event_fee)
        instance.is_event_fee_paid = validated_data.get('is_event_fee_paid', instance.is_event_fee_paid)
        instance.save()

        return instance


class RegistrationGroupSerializer(serializers.ModelSerializer):

    signed_up_by = SimpleMemberSerializer()
    registrations = RegistrationSerializer(many=True)

    class Meta:
        model = RegistrationGroup
        fields = ("id", "event", "signed_up_by", "notes", "payment_confirmation_code",
                  "payment_confirmation_timestamp", "payment_amount", "card_verification_token", "registrations", )

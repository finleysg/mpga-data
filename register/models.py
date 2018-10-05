from django.db import models
from django.db.models import CASCADE, DO_NOTHING
from simple_history.models import HistoricalRecords

from events.models import Event
from core.models import Member


class RegistrationGroup(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, on_delete=CASCADE)
    signed_up_by = models.ForeignKey(verbose_name="Signed up by", to=Member, on_delete=DO_NOTHING)
    notes = models.TextField(verbose_name="Registration notes", blank=True)
    card_verification_token = models.CharField(verbose_name="Card verification token", max_length=30, blank=True)
    payment_confirmation_code = models.CharField(verbose_name="Payment confirmation code", max_length=30, blank=True)
    payment_confirmation_timestamp = models.DateTimeField(verbose_name="Payment confirmation timestamp", blank=True, null=True)
    payment_amount = models.DecimalField(verbose_name="Payment amount", max_digits=5, decimal_places=2, blank=True, null=True)

    history = HistoricalRecords()

    @property
    def members(self):
        member_names = []
        for registration in self.registrations.all():
            if registration.member is not None:
                member_names.append(registration.member.member_name())
        return ", ".join(member_names)
    
    def __str__(self):
        return "{} group: {}".format(self.event.name, self.signed_up_by)


class Registration(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, related_name="registrations", on_delete=CASCADE)
    registration_group = models.ForeignKey(verbose_name="Group", to=RegistrationGroup, blank=True, null=True, on_delete=CASCADE, related_name="registrations")
    member = models.ForeignKey(verbose_name="Member", to=Member, blank=True, null=True, on_delete=DO_NOTHING)
    event_fee = models.DecimalField(verbose_name="Event fee", max_digits=5, decimal_places=2, blank=True, null=True)
    is_event_fee_paid = models.BooleanField(verbose_name="Event fee paid", default=False)

    history = HistoricalRecords()

    def __str__(self):
        return self.status

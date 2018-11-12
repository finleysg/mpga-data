from django.db import models
from django.db.models import CASCADE, DO_NOTHING
from simple_history.models import HistoricalRecords

from clubs.models import Club
from events.models import Event, EventDivision, EventFee
from core.models import Member


class Participant(models.Model):
    member = models.ForeignKey(verbose_name="Member", to=Member, blank=True, null=True,  on_delete=DO_NOTHING)
    home_club = models.ForeignKey(verbose_name="Home club", to=Club, blank=True, null=True, on_delete=DO_NOTHING)
    last_name = models.CharField(verbose_name="Last name", max_length=30)
    first_name = models.CharField(verbose_name="First name", max_length=30)
    email = models.CharField(verbose_name="Player email", max_length=240)
    ghin = models.CharField(verbose_name="GHIN", max_length=7)

    history = HistoricalRecords()

    def __str__(self):
        return "{} {} ({})".format(self.last_name, self.first_name, self.home_club.name)


class RegistrationGroup(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, on_delete=CASCADE)
    division = models.ForeignKey(verbose_name="Division", to=EventDivision, blank=True, null=True, on_delete=DO_NOTHING)
    registered_by = models.CharField(verbose_name="Registered_by", max_length=60, default="unknown")
    notes = models.TextField(verbose_name="Registration notes", blank=True)
    card_verification_token = models.CharField(verbose_name="Card verification token", max_length=30, blank=True)
    payment_confirmation_code = models.CharField(verbose_name="Payment confirmation code", max_length=30, blank=True)
    payment_confirmation_timestamp = models.DateTimeField(verbose_name="Payment confirmation timestamp", blank=True, null=True)
    payment_amount = models.DecimalField(verbose_name="Payment amount", max_digits=5, decimal_places=2, blank=True, null=True)

    history = HistoricalRecords()

    @property
    def players(self):
        names = []
        for registration in self.registrations.all():
            if registration.participant is not None:
                names.append(registration.participant.last_name)
        return ", ".join(names)
    
    def __str__(self):
        return "{} group: {}".format(self.event.name, self.registered_by)


class Registration(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, related_name="registrations", on_delete=CASCADE)
    registration_group = models.ForeignKey(verbose_name="Group", to=RegistrationGroup, blank=True, null=True, on_delete=CASCADE, related_name="registrations")
    participant = models.ForeignKey(verbose_name="Player", to=Participant, blank=True, null=True, on_delete=DO_NOTHING)
    event_fee = models.ForeignKey(verbose_name="Event fee", to=EventFee, on_delete=DO_NOTHING)
    is_event_fee_paid = models.BooleanField(verbose_name="Event fee paid", default=False)

    history = HistoricalRecords()

    def __str__(self):
        return "{} participant: {}".format(self.event.name, self.participant.last_name)

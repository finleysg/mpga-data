from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from datetime import datetime

from clubs.models import Club, Contact
from events.models import Event


class SeasonSettings(models.Model):
    year = models.IntegerField(verbose_name="Current golf season")
    reg_event = models.ForeignKey(verbose_name="Registration event", to=Event, on_delete=DO_NOTHING, related_name="registration")


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    home_club = models.ForeignKey(verbose_name="Home club", to=Club, blank=True, null=True, on_delete=DO_NOTHING)
    contact = models.ForeignKey(verbose_name="Contact", to=Contact, blank=True, null=True, on_delete=DO_NOTHING)
    ghin = models.CharField(verbose_name="GHIN", max_length=7, blank=True, null=True)
    birth_date = models.DateField(verbose_name="Birth date", blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ('user__last_name', 'user__first_name')

    def member_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def member_email(self):
        return self.user.email

    def has_email(self):
        return len(self.user.email) > 0 and \
               "@" in self.user.email and \
               not self.user.email.endswith("fake.com")

    def age(self):
        my_age = 0
        if self.birth_date:
            my_age = (datetime.utcnow() - self.birth_date).total_years()
        return my_age

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

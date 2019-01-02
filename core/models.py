from django.conf import settings
from django.db import models


class SeasonSettingsManager(models.Manager):
    def current_settings(self):
        return self.latest("event_calendar_year")


class SeasonSettings(models.Model):
    objects = SeasonSettingsManager()

    event_calendar_year = models.IntegerField(verbose_name="Default year for the event calendar")
    match_play_year = models.IntegerField(verbose_name="Default year for match play")
    member_club_year = models.IntegerField(verbose_name="Default year for club membership")
    membership_dues = models.IntegerField(verbose_name="Membership dues", default=100)

    @property
    def raven_dsn(self):
        return settings.RAVEN_DSN

    @property
    def stripe_public_key(self):
        return settings.STRIPE_PUBLIC_KEY

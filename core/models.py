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
    match_play_divisions = models.CharField(verbose_name="Match play divisions", max_length=150, default="")
    match_play_groups = models.CharField(verbose_name="Match play groups", max_length=250, default="")
    match_play_finalized = models.BooleanField(verbose_name="Match play teams are final", default=False)
    match_play_forfeit_percentage = models.DecimalField(verbose_name="Forfeit winner percentage",
                                                        decimal_places=1, max_digits=3, default=66.6)

    @property
    def raven_dsn(self):
        return settings.RAVEN_DSN

    @property
    def stripe_public_key(self):
        return settings.STRIPE_PUBLIC_KEY

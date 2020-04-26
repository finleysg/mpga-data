from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from simple_history.models import HistoricalRecords

from clubs.models import GolfCourse, Contact
from policies.models import Policy

EVENT_TYPE_CHOICES = (
    ("T", "Championship"),
    ("B", "Banquet"),
    ("M", "Meeting"),
    ("C", "Canceled"),
    ("P", "Postponed"),
)

REGISTRATION_TYPE_CHOICES = (
    ("1", "External"),
    ("2", "Internal"),
    ("3", "No Registration Required"),
)

LINK_TYPE_CHOICES = (
    ("Results", "Results"),
    ("Tee Times", "Tee Times"),
    ("Registration", "Registration"),
    ("Media", "Media"),
)

DIVISION_CHOICES = (
    ("Championship", "Championship"),
    ("Net", "Net"),
    ("Super-Senior", "Super-Senior"),
    ("Senior", "Senior"),
    ("Flighted", "Flighted"),
)


class Award(models.Model):
    name = models.CharField(verbose_name="Award Name", max_length=100)
    description = models.TextField(verbose_name="Description")

    def __str__(self):
        return self.name


class AwardWinner(models.Model):
    year = models.IntegerField(verbose_name="Year")
    award = models.ForeignKey(verbose_name="Award", to=Award, on_delete=DO_NOTHING, related_name="winners")
    winner = models.CharField(verbose_name="Award Winner", max_length=100)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    class Meta:
        ordering = ["-year", ]

    def __str__(self):
        return "{} {}".format(self.year, self.award)


class Tournament(models.Model):
    name = models.CharField(verbose_name="Tournament Name", max_length=100)
    system_name = models.CharField(verbose_name="System name", max_length=20, blank=True, null=True)
    description = models.TextField(verbose_name="Description")

    class Meta:
        verbose_name = 'Tournament'
        verbose_name_plural = 'Tournaments'

    def __str__(self):
        return self.name


class TournamentWinner(models.Model):
    year = models.IntegerField(verbose_name="Year")
    tournament = models.ForeignKey(verbose_name="Tournament", to=Tournament, on_delete=DO_NOTHING, related_name="winners")
    location = models.CharField(verbose_name="Location", max_length=100)
    winner = models.CharField(verbose_name="Winner", max_length=100)
    winner_club = models.CharField(verbose_name="Club", max_length=100, blank=True)
    co_winner = models.CharField(verbose_name="Winner (Opponent for Match Play)", max_length=100, blank=True)
    co_winner_club = models.CharField(verbose_name="Club", max_length=100, blank=True)
    flight_or_division = models.CharField(verbose_name="Flight or Division", max_length=20)
    score = models.CharField(verbose_name="Score", max_length=20, blank=True)
    is_net = models.BooleanField(verbose_name="Score is a Net Score", default=False)
    is_match = models.BooleanField(verbose_name="Match Play", default=False)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    class Meta:
        verbose_name = 'Tournament Winner'
        verbose_name_plural = 'Tournament Winners'
        ordering = ["-year", ]

    def __str__(self):
        return "{} {}".format(self.year, self.tournament)


class Event(models.Model):
    location = models.ForeignKey(verbose_name="Location", to=GolfCourse, on_delete=DO_NOTHING)
    tournament = models.ForeignKey(verbose_name="Championship", to=Tournament, on_delete=DO_NOTHING, blank=True, null=True)
    event_type = models.CharField(verbose_name="Event type", choices=EVENT_TYPE_CHOICES, max_length=1, default="T")
    name = models.CharField(verbose_name="Event title", max_length=100)
    description = models.TextField(verbose_name="Format and rules")
    notes = models.TextField(verbose_name="Additional notes", blank=True, null=True)
    start_date = models.DateField(verbose_name="Start date")
    rounds = models.IntegerField(verbose_name="Number of rounds", default=1)
    registration_start = models.DateTimeField(verbose_name="Registration start", blank=True, null=True)
    early_registration_end = models.DateTimeField(verbose_name="Early registration end", blank=True, null=True)
    registration_end = models.DateTimeField(verbose_name="Registration end", blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ["start_date", ]

    def __str__(self):
        return self.name


class EventChair(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, on_delete=CASCADE, related_name="chairs")
    chair = models.ForeignKey(verbose_name="Contact", to=Contact, on_delete=DO_NOTHING)

    def __str__(self):
        return "{}: {}".format(self.event.name, self.chair.last_name)


class EventPoints(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, on_delete=CASCADE, related_name="player_points")
    place = models.IntegerField(verbose_name="Place")
    points = models.IntegerField(verbose_name="Points")

    @property
    def ordinal_place(self):
        if self.place == 1:
            return "1st"
        elif self.place == 2:
            return "2nd"
        elif self.place == 3:
            return "3rd"
        else:
            return "{}th".format(self.place)

    def __str__(self):
        return "{}: {}".format(self.event.name, self.ordinal_place)


class EventPolicy(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, on_delete=models.CASCADE, related_name="policies")
    policy = models.ForeignKey(verbose_name="Policy", to=Policy, on_delete=models.CASCADE, related_name="policy_to_event")
    order = models.IntegerField(verbose_name="Display order")

    def __str__(self):
        return "{}: {}".format(self.event.name, self.policy.name)


class EventLink(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, on_delete=CASCADE, related_name="links")
    link_type = models.CharField(verbose_name="Link Type", max_length=40, choices=LINK_TYPE_CHOICES)
    title = models.CharField(verbose_name="Title", max_length=60, default="TM Portal")
    url = models.CharField(verbose_name="Full Url", max_length=240)

    def __str__(self):
        return "{}: {} link".format(self.event.name, self.link_type)

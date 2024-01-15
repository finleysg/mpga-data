from django.db import models
from simple_history.models import HistoricalRecords

PAGE_TYPE_CHOICES = (
    ("H", "Home"),
    ("B", "Tournament Bids"),
    ("A", "About the MPGA"),
    ("M", "Match Play"),
    ("C", "Member Clubs"),
    ("E", "Club Editing"),
    ("R", "Club Registration"),
    ("I", "Individual Registration"),
    ("CC", "Code of Conduct"),
    ("OM", "Our Mission"),
    ("EC", "Executive Committee"),
    ("MP", "Match Play Signup"),
    ("FQ", "FAQ"),
    ("PP", "Past Presidents"),
)


class LandingPage(models.Model):
    page_type = models.CharField(verbose_name="Type", choices=PAGE_TYPE_CHOICES, max_length=2)
    title = models.CharField(verbose_name="Title", max_length=120)
    content = models.TextField(verbose_name="Content")

    history = HistoricalRecords()

    def __str__(self):
        return self.title

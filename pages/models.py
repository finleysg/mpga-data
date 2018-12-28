from django.db import models
from simple_history.models import HistoricalRecords

PAGE_TYPE_CHOICES = (
    ("H", "Home"),
    ("B", "Tournament Bids"),
    ("A", "About the MPGA"),
    ("M", "Match Play"),
    ("C", "Member Clubs"),
    ("E", "Club Editing"),
    ("CC", "Code of Conduct"),
    ("OM", "Our Mission")
)


class LandingPage(models.Model):
    page_type = models.CharField(verbose_name="Type", choices=PAGE_TYPE_CHOICES, max_length=2)
    title = models.CharField(verbose_name="Title", max_length=120)
    content = models.TextField(verbose_name="Content")

    history = HistoricalRecords()

    def __str__(self):
        return self.title

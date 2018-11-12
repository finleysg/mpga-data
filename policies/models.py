from django.db import models
from simple_history.models import HistoricalRecords

POLICY_TYPE_CHOICES = (
    ("LR", "Local Rule"),
    ("CC", "Code of Conduct"),
    ("AU", "About Us"),
    ("SP", "Senior Match Play"),
    ("MP", "Match Play"),
    ("TN", "Tournament"),
    ("TP", "Tournament Player Information"),
    ("PP", "Pace of Play"),
    ("OX", "Other"),
)


class Policy(models.Model):
    policy_type = models.CharField(verbose_name="Type", choices=POLICY_TYPE_CHOICES, max_length=2, default="OX")
    name = models.CharField(verbose_name="Name", max_length=30)
    title = models.CharField(verbose_name="Title", max_length=120)
    description = models.TextField(verbose_name="Description")
    # version = models.IntegerField(verbose_name="Version", default=1)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'

    def __str__(self):
        return self.name

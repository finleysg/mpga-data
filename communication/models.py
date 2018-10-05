from django.db import models
from django.db.models import DO_NOTHING
from simple_history.models import HistoricalRecords
from events.models import Event
from documents.models import Document


class Announcement(models.Model):
    event = models.ForeignKey(verbose_name="Event", to=Event, blank=True, null=True, on_delete=DO_NOTHING)
    document = models.ForeignKey(verbose_name="Document", to=Document, blank=True, null=True, on_delete=DO_NOTHING)
    external_url = models.CharField(verbose_name="External url", max_length=255, blank=True)
    external_name = models.CharField(verbose_name="External url name", max_length=40, blank=True)
    title = models.CharField(verbose_name="Title", max_length=100)
    text = models.TextField(verbose_name="Announcement text")
    starts = models.DateTimeField(verbose_name="Display start")
    expires = models.DateTimeField(verbose_name="Display expiration")

    history = HistoricalRecords()

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    full_name = models.CharField(verbose_name="Full name", max_length=100)
    email = models.CharField(verbose_name="Email", max_length=254)
    message_text = models.TextField(verbose_name="Message text")
    message_date = models.DateTimeField(verbose_name="Message date", auto_now_add=True)

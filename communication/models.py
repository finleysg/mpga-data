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
    message_type = models.CharField(verbose_name="Message type", max_length=30)
    course = models.CharField(verbose_name="Golf course", blank=True, null=True, max_length=100)
    contact_name = models.CharField(verbose_name="Contact name", max_length=100)
    contact_email = models.CharField(verbose_name="Contact email", max_length=254)
    contact_phone = models.CharField(verbose_name="Contact phone", max_length=20)
    season = models.IntegerField(verbose_name="Golf season", blank=True, null=True)
    message = models.TextField(verbose_name="Message")
    message_date = models.DateTimeField(verbose_name="Message date", auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return "{}: {} {}".format(self.contact_name, self.message_type, self.message_date)

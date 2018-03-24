from django.db import models
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit

from clubs.models import GolfCourse

DOCUMENT_TYPE_CHOICES = (
    ("EA", "Event Application"),
    ("ER", "Event Results"),
    ("TT", "Event Tee Times"),
    ("SP", "Season Points"),
    ("MM", "Meeting Minutes"),
    ("MP", "Match Play"),
    ("F", "Financial Statements"),
    ("S", "Newsletter"),
    ("O", "Other")
)

PHOTO_TYPE_CHOICES = (
    ("GC", "Golf Course Photos"),
    ("EW", "Event Winners"),
    ("EP", "Event Photos"),
    ("O", "Other")
)


def document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "documents/{0}/{1}".format(instance.year, filename)


def photo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "photos/{0}/{1}".format(instance.year, filename)


class ThumbnailSpec(ImageSpec):
    format = 'JPEG'
    options = {'quality': 70}
    processors = [ResizeToFit(96, 96)]


class WebSpec(ImageSpec):
    format = 'JPEG'
    options = {'quality': 80}
    processors = [ResizeToFit(600, 600)]


class Event(models.Model):
    year = models.IntegerField(verbose_name="Golf Season", blank=True, null=True)
    month = models.CharField(verbose_name="Month", max_length=12)
    name = models.CharField(verbose_name="Name", max_length=100)
    location = models.ForeignKey(verbose_name="Location", to=GolfCourse, blank=True, null=True)
    portal_url = models.CharField(verbose_name="Portal URL", max_length=200, blank=True)

    def __str__(self):
        return "{} {}".format(self.year, self.name)


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag", max_length=40)

    def __str__(self):
        return self.name


class Document(models.Model):
    document_type = models.CharField(verbose_name="Document Type", choices=DOCUMENT_TYPE_CHOICES, max_length=2)
    year = models.IntegerField(verbose_name="Golf Season", blank=True, null=True)
    title = models.CharField(verbose_name="Title", max_length=120)
    event = models.ForeignKey(verbose_name="Event", to=Event, null=True, blank=True)
    file = models.FileField(verbose_name="File", upload_to=document_directory_path)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentTag(models.Model):
    document = models.ForeignKey(verbose_name="Document", to=Document)
    tag = models.ForeignKey(verbose_name="Tag", to=Tag)


class Photo(models.Model):
    photo_type = models.CharField(verbose_name="Type", choices=PHOTO_TYPE_CHOICES, max_length=2)
    year = models.IntegerField(verbose_name="Golf Season", default=0)
    title = models.CharField(verbose_name="Title", max_length=120)
    event = models.ForeignKey(verbose_name="Event", to=Event, null=True, blank=True)
    raw_image = models.ImageField(verbose_name="Image", upload_to=photo_directory_path)
    thumbnail_image = ImageSpecField(source="raw_image", id="web:image:thumbnail_image")
    web_image = ImageSpecField(source="raw_image", id="web:image:web_image")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PhotoTag(models.Model):
    document = models.ForeignKey(verbose_name="Photo", to=Photo)
    tag = models.ForeignKey(verbose_name="Tag", to=Tag)

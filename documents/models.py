from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit

from clubs.models import GolfCourse
from events.models import Event

DOCUMENT_TYPE_CHOICES = (
    ("T", "Tournament"),
    ("B", "Banquet"),
    ("M", "Meeting"),
    ("P", "Match Play"),
    ("F", "Financial"),
    ("C", "Communications"),
    ("O", "Other")
)

PHOTO_TYPE_CHOICES = (
    ("G", "Golf Course"),
    ("W", "Tournament Winners"),
    ("T", "Tournament Photos"),
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


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag", max_length=40)

    def __str__(self):
        return self.name


class Document(models.Model):
    document_type = models.CharField(verbose_name="Document Type", choices=DOCUMENT_TYPE_CHOICES, max_length=1)
    year = models.IntegerField(verbose_name="Golf Season", blank=True, null=True)
    title = models.CharField(verbose_name="Title", max_length=120)
    event = models.ForeignKey(verbose_name="Event", to=Event, null=True, blank=True, on_delete=DO_NOTHING, related_name="documents")
    file = models.FileField(verbose_name="File", upload_to=document_directory_path)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentTag(models.Model):
    document = models.ForeignKey(verbose_name="Document", to=Document, on_delete=CASCADE)
    tag = models.ForeignKey(verbose_name="Tag", to=Tag, on_delete=CASCADE)


class Photo(models.Model):
    photo_type = models.CharField(verbose_name="Type", choices=PHOTO_TYPE_CHOICES, max_length=1)
    year = models.IntegerField(verbose_name="Golf Season", default=0)
    title = models.CharField(verbose_name="Title", max_length=120)
    event = models.ForeignKey(verbose_name="Event", to=Event, null=True, blank=True, on_delete=DO_NOTHING)
    raw_image = models.ImageField(verbose_name="Image", upload_to=photo_directory_path)
    thumbnail_image = ImageSpecField(source="raw_image", id="web:image:thumbnail_image")
    web_image = ImageSpecField(source="raw_image", id="web:image:web_image")
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PhotoTag(models.Model):
    document = models.ForeignKey(verbose_name="Photo", to=Photo, on_delete=CASCADE)
    tag = models.ForeignKey(verbose_name="Tag", to=Tag, on_delete=CASCADE)

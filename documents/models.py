from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit, Transpose
from simple_history.models import HistoricalRecords

from documents.managers import PhotoManager, DocumentManager
from events.models import Tournament

DOCUMENT_TYPE_CHOICES = (
    ("ByLaws", "ByLaws"),
    ("Club Registration", "Club Registration"),
    ("Registration", "Registration"),
    ("Results", "Results"),
    ("Agenda", "Agenda"),
    ("Minutes", "Minutes"),
    ("Match Play", "Match Play"),
    ("Match Play Brackets", "Match Play Brackets"),
    ("Financial", "Financial"),
    ("Standing Orders", "Standing Orders"),
    ("Tee Times", "Tee Times"),
    ("Other", "Other"),
    ("Hard Card", "Hard Card")
)

PHOTO_TYPE_CHOICES = (
    ("Committee", "Committee"),
    ("Golf Course", "Golf Course"),
    ("Tournament Winners", "Tournament Winners"),
    ("Tournament Photos", "Tournament Photos"),
    ("Other", "Other")
)


def document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "documents/{0}/{1}".format(instance.year, filename)


def photo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "photos/{0}/{1}".format(instance.year, filename)


class ThumbnailSpec(ImageSpec):
    format = 'JPEG'
    options = {'quality': 80}
    processors = [Transpose(Transpose.AUTO), ResizeToFit(450, 450)]


class WebSpec(ImageSpec):
    format = 'JPEG'
    options = {'quality': 80}
    processors = [Transpose(Transpose.AUTO), ResizeToFit(1200, 1200)]


register.generator("documents:photo:thumbnail_image", ThumbnailSpec)
register.generator("documents:photo:web_image", WebSpec)


class Tag(models.Model):

    class Meta:
        ordering = ["name", ]

    name = models.CharField(verbose_name="Tag", max_length=40)

    def __str__(self):
        return self.name


class Document(models.Model):

    class Meta:
        ordering = ["-year", "-last_update", ]

    document_type = models.CharField(verbose_name="Document Type", choices=DOCUMENT_TYPE_CHOICES, max_length=20)
    year = models.IntegerField(verbose_name="Golf Season", blank=True, null=True)
    title = models.CharField(verbose_name="Title", max_length=120)
    tournament = models.ForeignKey(verbose_name="Tournament", to=Tournament, null=True, blank=True, on_delete=DO_NOTHING, related_name="documents")
    file = models.FileField(verbose_name="File", upload_to=document_directory_path)
    created_by = models.CharField(verbose_name="Created By", max_length=100)
    last_update = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()
    objects = DocumentManager()

    def __str__(self):
        return "{} {}: {}".format(self.year, self.document_type, self.title)


class DocumentTag(models.Model):
    document = models.ForeignKey(verbose_name="Document", to=Document, on_delete=CASCADE, related_name="tags")
    tag = models.ForeignKey(verbose_name="Tag", to=Tag, on_delete=CASCADE)


class Photo(models.Model):
    photo_type = models.CharField(verbose_name="Type", choices=PHOTO_TYPE_CHOICES, max_length=20)
    year = models.IntegerField(verbose_name="Golf Season", default=0)
    caption = models.CharField(verbose_name="Caption", max_length=240, blank=True)
    tournament = models.ForeignKey(verbose_name="Tournament", to=Tournament, null=True, blank=True, on_delete=DO_NOTHING, related_name="photos")
    raw_image = models.ImageField(verbose_name="Image", upload_to=photo_directory_path)
    thumbnail_image = ImageSpecField(source="raw_image", id="documents:photo:thumbnail_image")
    web_image = ImageSpecField(source="raw_image", id="documents:photo:web_image")
    created_by = models.CharField(verbose_name="Created By", max_length=100)
    last_update = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()
    objects = PhotoManager()

    def __str__(self):
        return "{} {}: {}".format(self.year, self.photo_type, self.caption)


class PhotoTag(models.Model):
    document = models.ForeignKey(verbose_name="Photo", to=Photo, on_delete=CASCADE, related_name="tags")
    tag = models.ForeignKey(verbose_name="Tag", to=Tag, on_delete=CASCADE)

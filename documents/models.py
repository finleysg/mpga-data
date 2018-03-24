from django.db import models

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

# PHOTO_TYPE_CHOICES = (
#     ("GC", "Golf Course Photos"),
#     ("EW", "Event Winners"),
#     ("EP", "Event Photos"),
#     ("O", "Other")
# )


def document_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "documents/{0}/{1}".format(instance.year, filename)


# def photo_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
#     return "photos/{0}/{1}".format(instance.year, filename)


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag", max_length=40)

    def __str__(self):
        return self.name


class Document(models.Model):
    document_type = models.CharField(verbose_name="Document Type", choices=DOCUMENT_TYPE_CHOICES, max_length=2)
    year = models.IntegerField(verbose_name="Golf Season", blank=True, null=True)
    title = models.CharField(verbose_name="Title", max_length=120)
    event = models.CharField(verbose_name="Event", max_length=120, blank=True)
    file = models.FileField(verbose_name="File", upload_to=document_directory_path)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentTag(models.Model):
    document = models.ForeignKey(verbose_name="Document", to=Document)
    tag = models.ForeignKey(verbose_name="Tag", to=Tag)


# class Photo(models.Model):
#     photo_type = models.CharField(verbose_name="Type", choices=PHOTO_TYPE_CHOICES, max_length=2)
#     year = models.IntegerField(verbose_name="Golf Season", default=0)
#     title = models.CharField(verbose_name="Title", max_length=120)
#     event = models.CharField(verbose_name="Event", max_length=120, blank=True)
#     file = models.ImageField(verbose_name="Image", upload_to=photo_directory_path)
#     last_update = models.DateTimeField(auto_now=True)
#     tags = models.ManyToManyField(Tag)
#
#     def __str__(self):
#         return self.title

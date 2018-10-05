from django.contrib import admin
from .models import Document, Tag, DocumentTag, PhotoTag, Photo


class TagInline(admin.TabularInline):
    model = DocumentTag
    can_delete = True
    extra = 0


class PhotoTagInline(admin.TabularInline):
    model = PhotoTag
    can_delete = True
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    fields = ["year", "document_type", "event", "title", "file", ]
    inlines = [TagInline, ]
    exclude = ("tags",)
    list_display = ["year", "title", "event", "document_type", ]
    list_filter = ("year", "event", "document_type", )
    save_on_top = True


class TagAdmin(admin.ModelAdmin):
    fields = ["name", ]
    list_display = ["name", ]


class PhotoAdmin(admin.ModelAdmin):
    fields = ["year", "photo_type", "event", "title", "raw_image", ]
    inlines = [PhotoTagInline, ]
    list_display = ["year", "title", "event", "photo_type", ]
    list_filter = ("year", "event", "photo_type", )
    save_on_top = True


admin.site.register(Document, DocumentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Photo, PhotoAdmin)

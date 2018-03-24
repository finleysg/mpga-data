from django.contrib import admin
from .models import Document, Tag, DocumentTag, PhotoTag, Photo, Event


class TagInline(admin.TabularInline):
    model = DocumentTag
    can_delete = True
    extra = 3


class PhotoTagInline(admin.TabularInline):
    model = PhotoTag
    can_delete = True
    extra = 3


class EventAdmin(admin.ModelAdmin):
    fields = ['year', 'month', 'name', 'location', 'portal_url', ]
    list_display = ['year', 'name', 'location', ]
    list_filter = ('year', )
    save_on_top = True


class DocumentAdmin(admin.ModelAdmin):
    fields = ['year', 'document_type', 'title', 'file', ]
    inlines = [TagInline, ]
    exclude = ('tags',)
    list_display = ['year', 'title', 'document_type', ]
    list_filter = ('year', 'document_type', )
    save_on_top = True


class TagAdmin(admin.ModelAdmin):
    fields = ['name', ]
    list_display = ['name', ]


class PhotoAdmin(admin.ModelAdmin):
    fields = ['year', 'photo_type', 'title', 'raw_image', ]
    inlines = [PhotoTagInline, ]
    list_display = ['year', 'title', 'photo_type', ]
    list_filter = ('year', 'photo_type', )
    save_on_top = True


admin.site.register(Document, DocumentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Event, EventAdmin)

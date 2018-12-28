from django.contrib import admin
from .models import Announcement, ContactMessage


class AnnouncementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("title", "text", "starts", "expires", )
        }),
        ("Link to an event or document (optional)", {
            "fields": ("event", "document", )
        }),
        ("Link to an external site (optional)", {
            "fields": ("external_url", "external_name", )
        }),
    )
    list_display = ["starts", "expires", "title", ]
    list_filter = ("starts", )
    save_on_top = True


admin.site.register(Announcement, AnnouncementAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Contact", {
            "fields": ("contact_name", "contact_email", "contact_phone", )
        }),
        ("Message", {
            "fields": ("message_type", "message", ),
            # "readonly_fields": ("message_date", )
        }),
        ("Other", {
            "fields": ("course", "event", )
        }),
    )
    list_display = ["contact_name", "message_type", "message_date", ]
    list_filter = ("message_type", "message_date", )
    save_on_top = True


admin.site.register(ContactMessage, ContactMessageAdmin)

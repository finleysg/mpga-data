from django.contrib import admin

from .models import Club, Contact, ClubContact, Membership, Team


class ContactInline(admin.TabularInline):
    model = ClubContact
    can_delete = True
    extra = 0


class ClubAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (("name", "type_2", ), )
        }),
        (None, {
            "fields": ("website", "club_email", "club_phone", "notes", )
        }),
        ("Mailing Address", {
            "fields": ("address_txt", "city", "state", "zip", )
        }),
    )
    inlines = [ContactInline, ]
    exclude = ("contacts", )
    list_display = ["name", "city", "state", ]
    list_display_links = ("name", )
    list_filter = ("type_2", )
    ordering = ["name", ]
    search_fields = ["name", ]
    save_on_top = True


class ContactAdmin(admin.ModelAdmin):
    fields = ["first_name", "last_name", "contact_type", "email", "primary_phone", "alternate_phone", ]
    list_display = ["name", "email", "contact_type", ]
    list_display_links = ("name", )
    list_filter = ["contact_type", ]
    ordering = ["last_name", "first_name", ]
    search_fields = ["last_name", "first_name", ]


class MembershipAdmin(admin.ModelAdmin):
    fields = ["year", "club", "payment_date", "payment_type", "payment_code", "notes", ]
    readonly_fields = ["create_date", ]
    list_display = ["year", "club", "payment_type", "payment_date", ]
    list_display_links = ["year", ]
    list_filter = ["year", "payment_type", ]
    ordering = ["year", "club", ]


class TeamAdmin(admin.ModelAdmin):
    fields = ["year", "club", "contact", "group_name", "is_senior", ]
    list_display = ["year", "club", "group_name", "contact", ]
    list_display_links = ["year", ]
    list_filter = ["year", "group_name", "is_senior", ]
    ordering = ["year", "club", ]


admin.site.register(Club, ClubAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Team, TeamAdmin)

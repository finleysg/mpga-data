from django.contrib import admin

from .models import Club, Contact, ClubContact, Membership, Team, GolfCourse


class ContactInline(admin.TabularInline):
    model = ClubContact
    can_delete = True
    extra = 0


class GolfCourseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("name", "email", "phone", "website", "notes", )
        }),
        ("Mailing Address", {
            "fields": ("address_txt", "city", "state", "zip",)
        }),
    )
    list_display = ["name", "city", ]
    list_display_links = ("name", )
    ordering = ["name", ]
    search_fields = ["name", ]
    save_on_top = True


class ClubAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (("name", "type_2", ), "golf_course", "website", "notes", )
        }),
    )
    inlines = [ContactInline, ]
    exclude = ("contacts", )
    list_display = ["name", "type_2", ]
    list_display_links = ("name", )
    list_filter = ("type_2", )
    ordering = ["name", ]
    search_fields = ["name", ]
    save_on_top = True


class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("first_name", "last_name", "contact_type", )
        }),
        ("Contact Information", {
            "fields": ("email", "primary_phone", "alternate_phone", )
        }),
        ("Mailing Address", {
            "fields": ("address_txt", "city", "state", "zip",)
        }),
    )
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


admin.site.register(GolfCourse, GolfCourseAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Team, TeamAdmin)

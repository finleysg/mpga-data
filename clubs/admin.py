from datetime import datetime
from django.contrib import admin
import nested_admin

from clubs.mixins import DefaultFilterMixIn
from .models import *

# https://github.com/sehmaschine/django-grappelli/issues/214#issuecomment-247320636
current_season = datetime.today().year


class ContactRoleInline(nested_admin.NestedTabularInline):
    model = ClubContactRole
    extra = 0
    # sortable_field_name = "role"


class ContactInline(nested_admin.NestedTabularInline):
    model = ClubContact
    can_delete = True
    extra = 0
    inlines = [ContactRoleInline, ]
    raw_id_fields = ("contact", )
    autocomplete_lookup_fields = {
        "fk": ["contact", ]
    }


class GolfCourseAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("name", "email", "phone", "website", "notes", )
        }),
        ("Mailing Address", {
            "fields": ("address_txt", "city", "state", "zip",)
        }),
    )
    list_display = ["name", "city", "phone", "email", ]
    list_display_links = ("name", )
    ordering = ["name", ]
    search_fields = ["name", ]
    save_on_top = True


class ClubAdmin(nested_admin.NestedModelAdmin):
    fieldsets = (
        (None, {
            "fields": (("name", "type_2", ), "golf_course", "website", "size", "notes", )
        }),
    )
    inlines = [ContactInline, ]
    exclude = ("contacts", )
    list_display = ["name", "golf_course", "size", "type_2", ]
    list_display_links = ("name", )
    list_filter = ("type_2", )
    ordering = ["name", ]
    search_fields = ["name", ]
    save_on_top = True
    raw_id_fields = ("golf_course", )
    autocomplete_lookup_fields = {
        "fk": ["golf_course", ]
    }


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
    list_display = ["last_name", "first_name", "email", "primary_phone", "contact_type", ]
    list_display_links = ("last_name", )
    list_filter = ["contact_type", ]
    ordering = ["last_name", "first_name", ]
    search_fields = ["last_name", "first_name", ]


class MembershipAdmin(DefaultFilterMixIn):
    fields = ["year", "club", "payment_date", "payment_type", "payment_code", "notes", ]
    readonly_fields = ["create_date", ]
    list_display = ["club", "payment_type", "payment_date", "year", ]
    list_display_links = ["club", ]
    list_filter = ["year", "payment_type", ]
    ordering = ["club", "year", ]
    default_filters = (f"year={current_season}", )
    raw_id_fields = ("club", )
    autocomplete_lookup_fields = {
        "fk": ["club", ]
    }


class TeamAdmin(DefaultFilterMixIn):
    fields = ["year", "club", "group_name", "is_senior", ]
    list_display = ["club", "group_name", "is_senior", "year", ]
    list_display_links = ["club", ]
    list_filter = ["year", "group_name", "is_senior", ]
    ordering = ["club", "year", ]
    default_filters = (f"year={current_season}", )
    change_list_filter_template = "admin/filter_listing.html"
    raw_id_fields = ("club", )
    autocomplete_lookup_fields = {
        "fk": ["club", ]
    }


class CommitteeAdmin(admin.ModelAdmin):
    fields = ["contact", "role", "home_club", ]
    list_display = ["contact", "role", "home_club", ]
    list_display_links = ["contact", ]
    ordering = ["contact", ]


class AffiliateAdmin(admin.ModelAdmin):
    fields = ["organization", "website", "notes", ]
    list_display = ["organization", "website", ]
    list_display_links = ["organization", ]
    ordering = ["organization", ]


admin.site.register(GolfCourse, GolfCourseAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Affiliate, AffiliateAdmin)

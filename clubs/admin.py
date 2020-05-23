from datetime import datetime
from django.contrib import admin
import nested_admin

from clubs.actions import ExportCsvMixin, ExportClubContactsMixin
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


class GolfCourseAdmin(admin.ModelAdmin, ExportCsvMixin):
    fieldsets = (
        (None, {
            "fields": ("name", "email", "phone", "website", "logo", "notes", )
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
    actions = ["export_as_csv", ]


class ClubAdmin(nested_admin.NestedModelAdmin, ExportCsvMixin):
    fieldsets = (
        (None, {
            "fields": (("name", ), "system_name", "golf_course", "website", "size", "notes", )
        }),
    )
    inlines = [ContactInline, ]
    exclude = ("contacts", )
    list_display = ["name", "system_name", "golf_course", "size", "website", ]
    list_editable = ["system_name", "size", "website", ]
    list_display_links = ("name", )
    ordering = ["name", ]
    search_fields = ["name", ]
    save_on_top = True
    actions = ["export_as_csv", ]


class ContactAdmin(admin.ModelAdmin, ExportCsvMixin):
    fieldsets = (
        (None, {
            "fields": ("first_name", "last_name", )
        }),
        ("Contact Information", {
            "fields": ("email", "send_email", "home_club", "primary_phone", "alternate_phone", )
        }),
        ("Mailing Address", {
            "fields": ("address_txt", "city", "state", "zip",)
        }),
    )
    list_display = ["last_name", "first_name", "email", "send_email", "home_club", "primary_phone", ]
    list_editable = ["email", "home_club", "primary_phone", ]
    list_display_links = ("last_name", )
    ordering = ["last_name", "first_name", ]
    search_fields = ["last_name", "first_name", "email", ]
    actions = ["export_as_csv", ]


class MembershipAdmin(DefaultFilterMixIn, ExportCsvMixin):
    fields = ["year", "club", "payment_date", "payment_type", "payment_code", "notes", ]
    readonly_fields = ["create_date", ]
    list_display = ["club", "payment_type", "payment_date", "year", ]
    list_display_links = ["club", ]
    list_filter = ["year", "payment_type", ]
    ordering = ["club", "year", ]
    default_filters = (f"year={current_season}", )
    actions = ["export_as_csv", ]


class TeamAdmin(DefaultFilterMixIn, ExportCsvMixin):
    fields = ["year", "club", "group_name", "is_senior", "notes", ]
    list_display = ["club", "year", "group_name", "is_senior", "notes", ]
    list_editable = ["group_name", "is_senior", ]
    list_display_links = ["club", ]
    list_filter = ["year", "group_name", "is_senior", ]
    ordering = ["club", "year", ]
    default_filters = (f"year={current_season}", )
    change_list_filter_template = "admin/filter_listing.html"
    actions = ["export_as_csv", ]


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


class MatchPlayResultAdmin(admin.ModelAdmin, ExportCsvMixin):
    fields = ["group_name", "match_date", "home_team", "home_team_score", "away_team", "away_team_score", "notes",
              "forfeit", "entered_by", ]
    list_display = ["group_name", "match_date", "home_team", "home_team_score", "away_team", "away_team_score",
                    "forfeit", "notes", ]
    list_display_links = ["group_name", "match_date", ]
    list_filter = ["group_name", "match_date", "forfeit", ]
    ordering = ["group_name", "match_date", ]
    actions = ["export_as_csv", ]


@admin.register(ClubContact)
class ClubContactAdmin(admin.ModelAdmin, ExportClubContactsMixin):
    fields = ["club", "contact", "user", "is_primary", "use_for_mailings", "notes", ]
    list_display = ["club", "contact", "is_primary", "use_for_mailings", ]
    list_display_links = ["club", "contact", ]
    ordering = ["club", "contact", ]
    actions = ["export_captains", "export_primary_contacts", "export_mailings", ]
    list_max_show_all = 500


admin.site.register(GolfCourse, GolfCourseAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(MatchPlayResult, MatchPlayResultAdmin)

from django.contrib import admin
from .models import *


class PolicyInline(admin.TabularInline):
    model = EventPolicy
    can_delete = True
    extra = 0
    verbose_name_plural = "policies"
    fields = ["policy", "order", ]


class PointsInline(admin.TabularInline):
    model = EventPoints
    can_delete = True
    extra = 0
    fields = ["place", "points", ]


class LinksInLine(admin.TabularInline):
    model = EventLink
    can_delete = True
    extra = 0
    fields = ["link_type", "title", "url", ]


class ChairInline(admin.TabularInline):
    model = EventChair
    can_delete = True
    extra = 0
    fields = ["chair", ]


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Basic Settings", {
            "fields": ("name", "location", ("event_type", "tournament", "start_date", "rounds", ), )
        }),
        ("Format and Notes", {
            "classes": ("wide",),
            "fields": ("description", "notes", )
        }),
        ("Registration", {
            "fields":  ("registration_start", "early_registration_end", "registration_end", ),
        }),
    )

    inlines = [PolicyInline, PointsInline, ChairInline, LinksInLine, ]
    list_display = ["name", "start_date", ]
    list_display_links = ("name", )
    list_filter = ("start_date", "event_type", )
    ordering = ["start_date", ]
    save_on_top = True
    save_as = True


class AwardAdmin(admin.ModelAdmin):
    fields = ["name", "description", ]
    list_display = ["name", ]
    save_on_top = True


class TournamentAdmin(admin.ModelAdmin):
    fields = ["name", "system_name", "description", ]
    list_display = ["name", "system_name", ]
    save_on_top = True


class AwardWinnerAdmin(admin.ModelAdmin):
    fields = ["award", "year", "winner", "notes", ]
    list_display = ["year", "award", "winner", ]
    list_filter = ("year", "award", )
    save_on_top = True


class TournamentWinnerAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Championship", {
            "fields": ("year", "tournament", "location", )
        }),
        ("Winners", {
            "fields":  (("winner", "winner_club", ),
                        ("co_winner", "co_winner_club", ),
                        ("flight_or_division", "score", "is_net", "is_match", ), )
        }),
        ("Notes", {
            "fields": ("notes", )
        }),
    )
    list_display = ["year", "tournament", "location", "winner", "winner_club", "co_winner", "co_winner_club",
                    "flight_or_division", ]
    list_filter = ("year", "tournament", "flight_or_division", "is_net", )
    save_on_top = True


admin.site.register(Event, EventAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(AwardWinner, AwardWinnerAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentWinner, TournamentWinnerAdmin)

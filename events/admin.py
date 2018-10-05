from django.contrib import admin

from .models import *


class PolicyInline(admin.StackedInline):
    model = EventPolicy
    can_delete = True
    extra = 0
    verbose_name_plural = "policies"
    fields = ["policy", "order", ]


class PointsInline(admin.StackedInline):
    model = EventPoints
    can_delete = True
    extra = 0
    fields = ["place", "points", ]


class ChairInline(admin.StackedInline):
    model = EventChair
    can_delete = True
    extra = 0
    fields = ["chair", ]


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Basic Settings and Fees", {
            "fields": ("name", "location", ("event_type", "tournament", "start_date", "rounds", ),
                       ("event_fee", "alt_event_fee", ), )
        }),
        ("Format and Notes", {
            "classes": ("wide",),
            "fields": ("description", "notes", )
        }),
        ("Registration", {
            "fields":  (("registration_start", "early_registration_end", "registration_end", ),
                       ("registration_maximum", "minimum_signup_group_size", "maximum_signup_group_size", ))
        }),
        ("Other", {
            "fields": ("registration_url", "portal_url", )
        }),
    )

    inlines = [PolicyInline, PointsInline, ChairInline, ]
    list_display = ["name", "start_date", ]
    list_display_links = ("name", )
    list_filter = ("start_date", "event_type", )
    ordering = ["start_date", ]
    save_on_top = True


class AwardAdmin(admin.ModelAdmin):
    fields = ["name", "description", ]
    list_display = ["name", ]
    save_on_top = True


class TournamentAdmin(admin.ModelAdmin):
    fields = ["name", "description", ]
    list_display = ["name", ]
    save_on_top = True


class AwardWinnerAdmin(admin.ModelAdmin):
    fields = ["award", "year", "winner", "notes", ]
    list_display = ["year", "award", "winner", ]
    list_filter = ("year", "award", )
    save_on_top = True


class TournamentWinnerAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Event", {
            "fields": ("year", "tournament", "location", )
        }),
        ("Winners", {
            "fields":  (("winner", "winner_club", ),
                        ("co_winner", "co_winner_club", ),
                        ("flight_or_division", "score", "is_net", ), )
        }),
        ("Notes", {
            "fields": ("notes", )
        }),
    )
    list_display = ["year", "tournament", "winner", "co_winner", ]
    list_filter = ("year", "tournament", )
    save_on_top = True


admin.site.register(Event, EventAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(AwardWinner, AwardWinnerAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentWinner, TournamentWinnerAdmin)

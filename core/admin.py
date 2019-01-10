from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import SeasonSettings


# class MemberInline(admin.StackedInline):
#     model = Member
#     can_delete = False
#     verbose_name_plural = "member"
#     fields = ["home_club", "contact", ]


# class MpgaUserAdmin(UserAdmin):
#     # inlines = (MemberInline, )
#     save_on_top = True


class SettingsAdmin(admin.ModelAdmin):
    fields = ["event_calendar_year", "match_play_year", "member_club_year", "membership_dues", "match_play_finalized", ]
    list_display = ["event_calendar_year", ]
    can_delete = False


# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, MpgaUserAdmin)
admin.site.register(SeasonSettings, SettingsAdmin)

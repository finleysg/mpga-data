import logging

from django.contrib import admin

from core.models import SeasonSettings
from events.models import Event
from .models import RegistrationGroup, Registration


class RegistrationInline(admin.TabularInline):
    model = Registration
    can_delete = True
    extra = 0
    fields = ["participant", "is_event_fee_paid", "event_fee", ]


class RegistrationGroupAdmin(admin.ModelAdmin):
    model = RegistrationGroup
    can_delete = True
    save_on_top = True

    fieldsets = (
        (None, {
            "fields": (("event", "registered_by", ), )
        }),
        ("Payment Information", {
            "fields": ("payment_amount", "payment_confirmation_code", "payment_confirmation_timestamp", )
        }),
        ("Notes", {
            "fields": ("notes", )
        })
    )
    inlines = [RegistrationInline, ]

    list_display = ["id", "registered_by", "players", "payment_confirmation_timestamp", "event", ]
    list_display_links = ("id", )
    list_select_related = ("registered_by", "event", )
    ordering = ["registered_by"]
    #
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     if db_field.name == "event":
    #         kwargs["queryset"] = Event.objects.filter(start_date__year=config.year)
    #     return super(RegistrationGroupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["registered_by"] = request.user.member.id
        if "_changelist_filters" in request.GET:
            filters = request.GET["_changelist_filters"]
            initial["event"] = filters.split("=")[1]
        return initial

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event_id = instance.registration_group.event_id
            instance.save()
        formset.save_m2m()


admin.site.register(RegistrationGroup, RegistrationGroupAdmin)

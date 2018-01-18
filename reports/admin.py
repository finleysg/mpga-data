from django.contrib import admin
from .models import TeamCaptains, AllContacts, PrimaryContacts
from .actions import export_contacts, export_captains


class ContactsAdmin(admin.ModelAdmin):
    exclude = ("vkey", )
    readonly_fields = ["name", "first_name", "last_name", "email", "primary_phone", "alternate_phone",
                       "contact_type", "role", "is_primary", ]
    list_display = ["name", "role", "first_name", "last_name", "is_primary", ]
    list_display_links = ["name", ]
    list_filter = ["role", "is_primary", ]
    ordering = ["name", "role", ]
    actions = [export_contacts, ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['title'] = 'View Contact'
        return super(ContactsAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


class TeamCaptainsAdmin(admin.ModelAdmin):
    exclude = ("vkey", "is_senior")
    readonly_fields = ["year", "name", "first_name", "last_name", "email", "primary_phone", "alternate_phone",
                       "contact_type", "group_name", ]
    list_display = ["year", "name", "group_name", "first_name", "last_name" ]
    list_display_links = ["year", ]
    list_filter = ["year", "group_name", "is_senior", ]
    ordering = ["year", "name", "group_name", ]
    actions = [export_captains, ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['title'] = 'View Team Captain'
        return super(TeamCaptainsAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


admin.site.register(PrimaryContacts, ContactsAdmin)
admin.site.register(AllContacts, ContactsAdmin)
admin.site.register(TeamCaptains, TeamCaptainsAdmin)

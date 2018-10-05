from django.contrib import admin
from policies.models import Policy


class PolicyAdmin(admin.ModelAdmin):
    fields = ["policy_type", "version", "name", "title", "description", ]
    list_display = ["name", "title", "policy_type", ]
    list_filter = ("policy_type", )
    save_on_top = True


admin.site.register(Policy, PolicyAdmin)

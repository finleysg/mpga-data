from django.contrib import admin
from .models import LandingPage


class LandingPageAdmin(admin.ModelAdmin):
    fields = ["page_type", "title", "content", ]
    list_display = ["title", "page_type", ]
    save_on_top = True


admin.site.register(LandingPage, LandingPageAdmin)

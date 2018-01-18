import csv

from django.http import HttpResponse


def export_contacts(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename='contacts.csv'"
    writer = csv.writer(response)
    writer.writerow(["Club", "First Name", "Last Name", "Email", "Primary Phone", "Alternate Phone", "Contact Type", "Role", ])
    contacts = queryset.values_list("name", "first_name", "last_name", "email", "primary_phone", "alternate_phone", "contact_type", "role", )
    for contact in contacts:
        writer.writerow(contact)
    return response


export_contacts.short_description = "Export to CSV"


def export_captains(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename='captains.csv'"
    writer = csv.writer(response)
    writer.writerow(["Club", "First Name", "Last Name", "Email", "Primary Phone", "Alternate Phone", "Group", ])
    captains = queryset.values_list("name", "first_name", "last_name", "email", "primary_phone", "alternate_phone", "group_name", )
    for captain in captains:
        writer.writerow(captain)
    return response


export_captains.short_description = "Export to CSV"

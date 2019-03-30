import csv

from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ExportClubContactsMixin:
    def export_captains(self, request, queryset):

        meta = self.model._meta
        field_names = ["Club", "Captain", "Email", "Phone", "Roles", "Notes", ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Captains.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            roles = ",".join([r.role for r in obj.roles.filter(role__contains="Captain")])
            if roles:
                row = writer.writerow([obj.club, "{} {}".format(obj.contact.first_name, obj.contact.last_name),
                                      obj.contact.email, obj.contact.primary_phone, roles, obj.notes, ])

        return response

    export_captains.short_description = "Export Captains"

    def export_primary_contacts(self, request, queryset):

        meta = self.model._meta
        field_names = ["Club", "Contact", "Email", "Phone", "Roles", "Notes", ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=PrimaryContacts.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            roles = ",".join([r.role for r in obj.roles.all()])
            if obj.is_primary:
                row = writer.writerow([obj.club, "{} {}".format(obj.contact.first_name, obj.contact.last_name),
                                       obj.contact.email, obj.contact.primary_phone, roles, obj.notes, ])

        return response

    export_primary_contacts.short_description = "Export Primary Contacts"

    def export_mailings(self, request, queryset):

        meta = self.model._meta
        field_names = ["Club", "Contact", "Address", "City", "State", "Zip", ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=ClubMailingAddresses.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            if obj.use_for_mailings:
                row = writer.writerow([obj.club, "{} {}".format(obj.contact.first_name, obj.contact.last_name),
                                       obj.contact.address_txt, obj.contact.city, obj.contact.state,
                                       obj.contact.zip, ])

        return response

    export_mailings.short_description = "Export Mailing Addresses"

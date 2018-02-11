import csv

from django.http import HttpResponse

from clubs.models import ClubContact


def export_addresses(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename='addresses.csv'"
    writer = csv.writer(response)
    writer.writerow(["Club", "Address", "City", "State", "Zip", "Contact", ])
    clubs = queryset.values_list("name", "address_txt", "city", "state", "zip", "id", )
    for club in clubs:
        clubcontacts = ClubContact.objects.filter(club_id=club[5]).filter(is_primary=True)
        if len(clubcontacts) == 1:
            club = club[:-1] + ("{} {}".format(clubcontacts[0].contact.first_name, clubcontacts[0].contact.last_name), )
            writer.writerow(club)
        else:
            for contact in clubcontacts:
                if contact.contact.contact_type == "Facilities":
                    contact_name = "{} {}".format(contact.contact.first_name, contact.contact.last_name)
                    club = club[:-1] + (contact_name, )
                    writer.writerow(club)
    return response


export_addresses.short_description = "Export Addresses"
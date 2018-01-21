import csv

from django.http import HttpResponse
from templated_email import send_templated_mail, get_templated_mail
from reports.models import AllContacts


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


def contact_confirmation(modeladmin, request, queryset):
    secretary_name = "Stuart Finley"
    secretary_email = "finleysg@gmail.com"
    intro_text_a = ("You are receiving this email because the MPGA has you listed as a primary contact for "
                    "your club. We are asking for your help to ensure our records are correct and that we "
                    "contact the correct people throughout the upcoming golf season.")
    intro_text_b = ("Please take a moment to review the contact list below that we have for your club. "
                    "If there are any changes or corrections, you can simply respond to this email with "
                    "that information. We would also like your 2018 club president information if that "
                    "has changed or if we do not currently have your president listed below.")

    clubs = queryset.all()
    for club in clubs:
        contacts = AllContacts.objects.filter(name=club.club.name)
        for contact in contacts:
            if contact.is_primary:
                context = {
                    "club_name": club.club.name,
                    "secretary_name": secretary_name,
                    "secretary_email": secretary_email,
                    "intro_text_a": intro_text_a,
                    "intro_text_b": intro_text_b,
                    "greeting": "Dear " + contact.first_name,
                    "contacts": get_contacts_to_confirm(contacts)
                }
                send_templated_mail(
                    template_name="contact_confirmation",
                    template_suffix="email",
                    from_email=secretary_email,
                    recipient_list=[contact.email, ],
                    context=context
                )


contact_confirmation.short_description = "Create Contact Confirmation Emails"


def get_role_text(contact):
    if contact.is_primary:
        return "{} (Primary Contact)".format(contact.role)
    else:
        return contact.role


def update_greeting(contact, greeting):
    if contact.is_primary and len(greeting) == 0:
        return "Dear " + contact.first_name
    elif contact.is_primary and len(greeting) > 0:
        return greeting + " and " + contact.first_name
    else:
        return greeting


def get_contacts_to_confirm(contacts):
    email_contacts = []
    for contact in contacts:
        email_contacts.append({
            "role_text": get_role_text(contact),
            "contact_name": "{} {}".format(contact.first_name, contact.last_name),
            "email": contact.email,
            "primary_phone": contact.primary_phone if contact.primary_phone else "missing",
            "alternate_phone": contact.alternate_phone
        })
    return email_contacts

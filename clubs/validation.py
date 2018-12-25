from clubs.models import ClubContact

all_club_contacts = list(ClubContact.objects.values_list("contact", "id", "club__name"))


def check_club(club):

    messages = []
    if not club.size:
        messages.append(("warning", "Missing club size. We use the size of the club to award the Earl Wortman trophy."))
    if not club.notes:
        messages.append(("info", "Use the club notes to share information about your club."))
    if not club.club_contacts:
        messages.append(("error", "Please give us at least one club contact."))
    if not has_handicap_chair(club):
        messages.append(("error", "Every club must have a Handicap Chair."))

    for cc in club.club_contacts.all():
        messages.extend(check_club_contact(cc))

    return messages


def has_handicap_chair(club):
    # from https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    # [item for sublist in l for item in sublist], which is that same as
    # for sublist in l:
    #     for item in sublist:
    #         flat_list.append(item)
    all_roles = []  # [role.name for cc in club.club_contacts for role in cc.roles]
    for cc in club.club_contacts.all():
        for role in cc.roles.all():
            all_roles.append(role.role)
    handicap_chair = [r for r in all_roles if r == "Handicap Chair"]
    return len(handicap_chair) > 0


def check_club_contact(cc):

    messages = []
    contact_name = "{} {}".format(cc.contact.first_name, cc.contact.last_name)
    
    # ensure the contact is associated with a single club
    contacts = [c for c in all_club_contacts if c[0] == cc.contact.id]
    if len(contacts) > 1:
        messages.append(
            ("warning",
             "{} is a contact in {} different clubs: {}".format(
                 contact_name, len(contacts), ", ".join([c[2] for c in contacts]))))

    if not cc.roles.all():
        messages.append(("error", "{} does not have an assigned role in your club.".format(contact_name)))

    # contact details
    if cc.use_for_mailings and not cc.contact.has_address:
        messages.append(("error",
                         "We cannot send mailings to {} because the address is incomplete".format(contact_name)))

    if not cc.contact.email:
        messages.append(("error", "{} is missing an email address.".format(contact_name)))

    if not cc.contact.primary_phone:
        messages.append(("warning", "{} is missing a phone number".format(contact_name)))

    return messages

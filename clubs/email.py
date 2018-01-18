from .models import Club, Contact, Team


def generate_contact_confirmation(club):

    primary_mc_contact = club.contacts.filter("is_primary" == True and "contact__type" == "MC")
    match_play_caption = club.teams.filter("year" == 2017 and "is_senior" == False)

    return "test"

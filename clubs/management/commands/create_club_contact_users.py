from django.core.management.base import BaseCommand
from clubs.models import Club


class Command(BaseCommand):
    help = "Create user records for club contacts with email addresses"

    def handle(self, *args, **options):
        clubs = Club.objects.all()

        for club in clubs:
            contacts = club.club_contacts.exclude(contact__email__isnull=True).all()
            count = 0
            for contact in contacts:
                try:
                    # rely on the model save customization that creates/updates a user
                    contact.is_primary = not contact.is_primary
                    contact.save()
                    contact.is_primary = not contact.is_primary
                    contact.save()
                    count += 1
                except Exception as e:
                    print(e)

            self.stdout.write(self.style.SUCCESS("updated {} contacts for {}".format(count, club.name)))

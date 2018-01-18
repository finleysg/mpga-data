from django.db import models

# These are all models over views


class PrimaryContacts(models.Model):

    class Meta:
        verbose_name_plural = "Primary Contacts"
        db_table = "club_contacts_view"
        managed = False

    vkey = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(verbose_name="Club Name", max_length=200)
    first_name = models.CharField(verbose_name="First Name", max_length=30)
    last_name = models.CharField(verbose_name="Last Name", max_length=30)
    contact_type = models.CharField(verbose_name="Contact Type", max_length=3)
    primary_phone = models.CharField(verbose_name="Primary Phone", max_length=20, blank=True)
    alternate_phone = models.CharField(verbose_name="Alternate Phone", max_length=20, blank=True)
    email = models.CharField(verbose_name="Email", max_length=250, blank=True)
    role = models.CharField(verbose_name="Role", max_length=30)
    is_primary = models.BooleanField(verbose_name="Primary")

    def __str__(self):
        return "{} - {}: {} {}".format(self.name, self.role, self.first_name, self.last_name)


class AllContacts(models.Model):

    class Meta:
        verbose_name_plural = "All Contacts"
        db_table = "all_contacts_view"
        managed = False

    vkey = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(verbose_name="Club Name", max_length=200)
    first_name = models.CharField(verbose_name="First Name", max_length=30)
    last_name = models.CharField(verbose_name="Last Name", max_length=30)
    contact_type = models.CharField(verbose_name="Contact Type", max_length=3)
    primary_phone = models.CharField(verbose_name="Primary Phone", max_length=20, blank=True)
    alternate_phone = models.CharField(verbose_name="Alternate Phone", max_length=20, blank=True)
    email = models.CharField(verbose_name="Email", max_length=250, blank=True)
    role = models.CharField(verbose_name="Role", max_length=30)
    is_primary = models.BooleanField(verbose_name="Primary")

    def __str__(self):
        return "{} - {}: {} {}".format(self.name, self.role, self.first_name, self.last_name)


class TeamCaptains(models.Model):

    class Meta:
        verbose_name_plural = "Team Captains"
        db_table = "team_captains_view"
        managed = False

    vkey = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(verbose_name="Club Name", max_length=200)
    first_name = models.CharField(verbose_name="First Name", max_length=30)
    last_name = models.CharField(verbose_name="Last Name", max_length=30)
    contact_type = models.CharField(verbose_name="Contact Type", max_length=3)
    primary_phone = models.CharField(verbose_name="Primary Phone", max_length=20, blank=True)
    alternate_phone = models.CharField(verbose_name="Alternate Phone", max_length=20, blank=True)
    email = models.CharField(verbose_name="Email", max_length=250, blank=True)
    year = models.IntegerField(verbose_name="Golf Season")
    group_name = models.CharField(verbose_name="Group", max_length=20)
    is_senior = models.BooleanField(verbose_name="Senior")

    def __str__(self):
        return "{} {}: {}".format(self.year, self.group_name, self.name)

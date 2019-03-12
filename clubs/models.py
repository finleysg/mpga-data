import random
import string

from django.contrib.auth.models import User
from django.db import models
from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit

STATE_CHOICES = (
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
    ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'),
    ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
    ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
    ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'),
    ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
    ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
    ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'),
    ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
)

LOCAL_STATE_CHOICES = (
    ('IA', 'Iowa'), ('MN', 'Minnesota'), ('ND', 'North Dakota'), ('WI', 'Wisconsin')
)

CONTACT_TYPE_CHOICES = (
    ("Men's Club", "Men's Club"),
    ("Facilities", "Facilities"),
)

CONTACT_ROLE_CHOICES = (
    ("Director of Golf", "Director of Golf"),
    ("Event Director", "Event Director"),
    ("General Manager", "General Manager"),
    ("Handicap Chair", "Handicap Chair"),
    ("Manager", "Manager"),
    ("Match Play Captain", "Match Play Captain"),
    ("Men's Club Contact", "Men's Club Contact"),
    ("Men's Club President", "Men's Club President"),
    ("Men's Club Secretary", "Men's Club Secretary"),
    ("Men's Club Treasurer", "Men's Club Treasurer"),
    ("Owner", "Owner"),
    ("PGA Professional", "PGA Professional"),
    ("Sr. Match Play Captain", "Sr. Match Play Captain"),
    ("Superintendent", "Superintendent"),
    ("Other", "Other"),
)

PAYMENT_TYPE_CHOICES = (
    ("CK", "Check"),
    ("OL", "Online"),
    ("CA", "Cash"),
)


def photo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/year/<filename>
    return "photos/course-logos/{0}".format(filename)


class WebSpec(ImageSpec):
    format = 'JPEG'
    options = {'quality': 80}
    processors = [ResizeToFit(192, 192)]


register.generator("clubs:golf_course:web_logo", WebSpec)


class GolfCourse(models.Model):

    class Meta:
        ordering = ["name", ]

    name = models.CharField(verbose_name="Golf Course Name", max_length=200)
    address_txt = models.CharField(verbose_name="Street Address", max_length=200, blank=True)
    city = models.CharField(verbose_name="City", max_length=40, blank=True)
    state = models.CharField(verbose_name="State", max_length=2, choices=LOCAL_STATE_CHOICES, default="MN", blank=True)
    zip = models.CharField(verbose_name="Zip Code", max_length=10, blank=True)
    website = models.CharField(verbose_name="Website", max_length=300, blank=True)
    email = models.CharField(verbose_name="Email", max_length=250, blank=True)
    phone = models.CharField(verbose_name="Phone", max_length=20, blank=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)
    logo = models.ImageField(verbose_name="Logo", upload_to=photo_directory_path)
    web_logo = ImageSpecField(source="logo", id="clubs:golf_course:web_logo")

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", )


class Contact(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=30)
    last_name = models.CharField(verbose_name="Last Name", max_length=30)
    contact_type = models.CharField(verbose_name="Contact Type", max_length=20, choices=CONTACT_TYPE_CHOICES, default="Men's Club")
    primary_phone = models.CharField(verbose_name="Primary Phone", max_length=20, blank=True, null=True)
    alternate_phone = models.CharField(verbose_name="Alternate Phone", max_length=20, blank=True, null=True)
    email = models.CharField(verbose_name="Email", max_length=250, blank=True, null=True)
    address_txt = models.CharField(verbose_name="Street Address", max_length=200, blank=True, null=True)
    city = models.CharField(verbose_name="City", max_length=40, blank=True, null=True)
    state = models.CharField(verbose_name="State", max_length=2, choices=STATE_CHOICES, default="MN", blank=True, null=True)
    zip = models.CharField(verbose_name="Zip Code", max_length=10, blank=True, null=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    @property
    def public_email(self):
        if self.email:
            return "xxxxxx@{}".format(str(self.email).split("@")[1])
        else:
            return ""

    @property
    def public_primary_phone(self):
        if self.primary_phone:
            return "{}-xxx-xxxx".format(str(self.primary_phone).split("-")[0])
        else:
            return ""

    @property
    def public_alternate_phone(self):
        if self.alternate_phone:
            return "{}-xxx-xxxx".format(str(self.alternate_phone).split("-")[0])
        else:
            return ""

    @property
    def name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    @property
    def has_address(self):
        return self.address_txt and self.city and self.state and self.zip

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("last_name__icontains", )


class Club(models.Model):

    class Meta:
        ordering = ["name", ]

    name = models.CharField(verbose_name="Club Name", max_length=200)
    short_name = models.CharField(verbose_name="Short Name", max_length=50, blank=True, null=True)
    golf_course = models.ForeignKey(verbose_name="Home Course", blank=True, null=True, to=GolfCourse, on_delete=models.DO_NOTHING)
    website = models.CharField(verbose_name="Website", max_length=300, blank=True)
    type_2 = models.BooleanField(verbose_name="Type 2", default=False)
    size = models.IntegerField(verbose_name="Number of Members", blank=True, null=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)
    contacts = models.ManyToManyField(verbose_name="Contacts", to=Contact, through="ClubContact")

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", )


class ClubContact(models.Model):

    class Meta:
        ordering = ["contact__last_name", "contact__first_name", ]

    club = models.ForeignKey(verbose_name="Club", to=Club, on_delete=models.DO_NOTHING, related_name="club_contacts")
    contact = models.ForeignKey(verbose_name="Contact", to=Contact, on_delete=models.CASCADE, related_name="contact_to_club")
    user = models.ForeignKey(verbose_name="User", to=User, on_delete=models.CASCADE, blank=True, null=True)
    is_primary = models.BooleanField(verbose_name="Primary Contact", default=False)
    use_for_mailings = models.BooleanField(verbose_name="Use for Club Mailings", default=False)
    notes = models.CharField(verbose_name="Notes", max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):

        # create or update a user record only if we have an email address
        # this is to support password-less auth for temporary tokens
        if self.contact.email:
            uname = "".join([random.choice(string.ascii_lowercase) for n in range(24)])
            if not self.user:
                user = User.objects.filter(email=self.contact.email).first()
                if not user:
                    user = User.objects.create_user(username=uname,
                                                    email=self.contact.email,
                                                    password=uname,
                                                    first_name=self.contact.first_name,
                                                    last_name=self.contact.last_name)
                self.user = user
            else:
                user = User.objects.get(pk=self.user.id)
                user.email = self.contact.email
                if user.password.startswith('!'):  # i.e. no password set
                    user.set_password(uname)
                user.save()

        super().save(*args, **kwargs)

    # relying on a bit of a hack to ensure we don't delete an EC member
    def delete(self, *args, **kwargs):
        if self.user and len(self.user.username) == 24:
            self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return "{}: {} {}".format(self.club.name, self.contact.first_name, self.contact.last_name)


class ClubContactRole(models.Model):
    club_contact = models.ForeignKey(verbose_name="Club Contact", to=ClubContact, on_delete=models.CASCADE, related_name="roles")
    role = models.CharField(verbose_name="Role", max_length=30, choices=CONTACT_ROLE_CHOICES)

    def __str__(self):
        return "{} {}: {}".format(self.club_contact.contact.first_name, self.club_contact.contact.last_name, self.role)


class Membership(models.Model):
    class Meta:
        ordering = ["-year", "club__name", ]

    year = models.IntegerField(verbose_name="Golf Season")
    club = models.ForeignKey(verbose_name="Club", to=Club, on_delete=models.DO_NOTHING, related_name="memberships")
    payment_date = models.DateField(verbose_name="Payment Date")
    payment_type = models.CharField(verbose_name="Payment Type", max_length=2, choices=PAYMENT_TYPE_CHOICES, default="CK")
    payment_code = models.CharField(verbose_name="Code or Number", max_length=100, blank=True)
    create_date = models.DateTimeField(verbose_name="Date Recorded", auto_now_add=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    def __str__(self):
        return "{}: {} ({})".format(self.year, self.club.name, self.payment_date)


class Team(models.Model):
    year = models.IntegerField(verbose_name="Golf Season")
    club = models.ForeignKey(verbose_name="Club", to=Club, on_delete=models.DO_NOTHING, related_name="teams")
    group_name = models.CharField(verbose_name="Group", max_length=20)
    is_senior = models.BooleanField(verbose_name="Senior")
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    def __str__(self):
        return "{} {}: {}".format(self.year, self.group_name, self.club.name)


class MatchPlayResult(models.Model):
    group_name = models.CharField(verbose_name="Group", max_length=20)
    match_date = models.DateField(verbose_name="Date Played")
    home_team = models.ForeignKey(verbose_name="Home Team", to=Club, on_delete=models.DO_NOTHING, related_name="home_team")
    away_team = models.ForeignKey(verbose_name="Away Team", to=Club, on_delete=models.DO_NOTHING, related_name="away_team")
    home_team_score = models.DecimalField(verbose_name="Home Team Score", max_digits=3, decimal_places=1)
    away_team_score = models.DecimalField(verbose_name="Away Team Score", max_digits=3, decimal_places=1)
    entered_by = models.CharField(verbose_name="Entered By", max_length=60)
    forfeit = models.BooleanField(verbose_name="Forfeit")
    notes = models.CharField(verbose_name="Notes", max_length=140, blank=True, null=True)

    class Meta:
        ordering = ["-match_date", "group_name", ]

    def __str__(self):
        return "{} match on {}: {} vs {}".format(
            self.group_name, self.match_date, self.away_team.name, self.home_team.name)


class Committee(models.Model):
    class Meta:
        verbose_name = 'Executive Committee'
        verbose_name_plural = 'Executive Committee'

    contact = models.ForeignKey(verbose_name="Contact", to=Contact, on_delete=models.DO_NOTHING)
    role = models.CharField(verbose_name="Role", max_length=40)
    home_club = models.ForeignKey(verbose_name="Home Club", to=Club, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}: {} {}".format(self.role, self.contact.first_name, self.contact.last_name)


class Affiliate(models.Model):
    organization = models.CharField(verbose_name="Organization", max_length=60)
    website = models.CharField(verbose_name="Website", max_length=240)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    def __str__(self):
        return self.organization

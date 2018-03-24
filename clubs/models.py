from django.db import models


STATE_CHOICES = (
    ("IA", "Iowa"),
    ("MN", "Minnesota"),
    ("ND", "North Dakota"),
    ("SD", "South Dakota"),
    ("WI", "Wisconsin"),
)

CONTACT_TYPE_CHOICES = (
    ("Men's Club", "Men's Club"),
    ("Facilities", "Facilities"),
    ("Allied Association", "Allied Association"),
    ("Executive Committee", "Executive Committee"),
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
)

PAYMENT_TYPE_CHOICES = (
    ("CK", "Check"),
    ("OL", "Online"),
    ("CA", "Cash"),
)


class GolfCourse(models.Model):

    class Meta:
        ordering = ["name", ]

    name = models.CharField(verbose_name="Golf Course Name", max_length=200)
    address_txt = models.CharField(verbose_name="Street Address", max_length=200, blank=True)
    city = models.CharField(verbose_name="City", max_length=40, blank=True)
    state = models.CharField(verbose_name="State", max_length=2, choices=STATE_CHOICES, default="MN", blank=True)
    zip = models.CharField(verbose_name="Zip Code", max_length=10, blank=True)
    website = models.CharField(verbose_name="Website", max_length=300, blank=True)
    email = models.CharField(verbose_name="Email", max_length=250, blank=True)
    phone = models.CharField(verbose_name="Phone", max_length=20, blank=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=30)
    last_name = models.CharField(verbose_name="Last Name", max_length=30)
    contact_type = models.CharField(verbose_name="Contact Type", max_length=20, choices=CONTACT_TYPE_CHOICES, default="Men's Club")
    primary_phone = models.CharField(verbose_name="Primary Phone", max_length=20, blank=True)
    alternate_phone = models.CharField(verbose_name="Alternate Phone", max_length=20, blank=True)
    email = models.CharField(verbose_name="Email", max_length=250, blank=True)
    address_txt = models.CharField(verbose_name="Street Address", max_length=200, blank=True)
    city = models.CharField(verbose_name="City", max_length=40, blank=True)
    state = models.CharField(verbose_name="State", max_length=2, choices=STATE_CHOICES, default="MN", blank=True)
    zip = models.CharField(verbose_name="Zip Code", max_length=10, blank=True)

    def name(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def __str__(self):
        return self.name()


class Club(models.Model):

    class Meta:
        ordering = ["name", ]

    name = models.CharField(verbose_name="Club Name", max_length=200)
    golf_course = models.ForeignKey(verbose_name="Home Course", blank=True, null=True, to=GolfCourse, on_delete=models.DO_NOTHING)
    address_txt = models.CharField(verbose_name="Street Address", max_length=200, blank=True)
    city = models.CharField(verbose_name="City", max_length=40, blank=True)
    state = models.CharField(verbose_name="State", max_length=2, choices=STATE_CHOICES, default="MN", blank=True)
    zip = models.CharField(verbose_name="Zip Code", max_length=10, blank=True)
    website = models.CharField(verbose_name="Website", max_length=300, blank=True)
    club_email = models.CharField(verbose_name="Club Email", max_length=250, blank=True)
    club_phone = models.CharField(verbose_name="Club Phone", max_length=20, blank=True)
    type_2 = models.BooleanField(verbose_name="Type 2", default=False)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)
    contacts = models.ManyToManyField(verbose_name="Contacts", to=Contact, through="ClubContact")

    def __str__(self):
        return self.name


class ClubContact(models.Model):
    club = models.ForeignKey(verbose_name="Club", to=Club, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(verbose_name="Contact", to=Contact, on_delete=models.DO_NOTHING)
    role = models.CharField(verbose_name="Role", max_length=30, choices=CONTACT_ROLE_CHOICES)
    is_primary = models.BooleanField(verbose_name="Primary Contact", default=False)
    use_for_mailings = models.BooleanField(verbose_name="Use for Club Mailings", default=False)

    def __str__(self):
        return "{} {}: {}".format(self.contact.first_name, self.contact.last_name, self.role)


class Membership(models.Model):
    year = models.IntegerField(verbose_name="Golf Season")
    club = models.ForeignKey(verbose_name="Club", to=Club, on_delete=models.DO_NOTHING)
    payment_date = models.DateField(verbose_name="Payment Date")
    payment_type = models.CharField(verbose_name="Payment Type", max_length=2, choices=PAYMENT_TYPE_CHOICES, default="CK")
    payment_code = models.CharField(verbose_name="Code or Number", max_length=20, blank=True)
    create_date = models.DateTimeField(verbose_name="Date Recorded", auto_now_add=True)
    notes = models.TextField(verbose_name="Notes", blank=True, null=True)

    def __str__(self):
        return "{}: {} ({})".format(self.year, self.club.name, self.payment_date)


class Team(models.Model):
    year = models.IntegerField(verbose_name="Golf Season")
    club = models.ForeignKey(verbose_name="Club", to=Club, on_delete=models.DO_NOTHING, related_name="teams")
    contact = models.ForeignKey(verbose_name="Captain", to=Contact, on_delete=models.DO_NOTHING, null=True)
    group_name = models.CharField(verbose_name="Group", max_length=20)
    is_senior = models.BooleanField(verbose_name="Senior")

    def __str__(self):
        return "{} {}: {}".format(self.year, self.group_name, self.club.name)


class ContactImport(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=30)
    last_name = models.CharField(verbose_name="Last Name", max_length=30)
    address_txt = models.CharField(verbose_name="Street Address", max_length=200, blank=True)
    city = models.CharField(verbose_name="City", max_length=40, blank=True)
    state = models.CharField(verbose_name="State", max_length=2, choices=STATE_CHOICES, default="MN", blank=True)
    zip = models.CharField(verbose_name="Zip Code", max_length=10, blank=True)

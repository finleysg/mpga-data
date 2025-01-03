import os
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings as djoser_settings
from templated_email import send_templated_mail
from templated_email import InlineImage
from templated_mail.mail import BaseEmailMessage


logo_file = os.path.join(settings.BASE_DIR, "templates/templated_email/mpga-logo.jpg")
with open(logo_file, "rb") as logo:
    image = logo.read()
    inline_image = InlineImage(filename=logo_file, content=image)


def forward_contact_message(message):

    send_templated_mail(
        template_name=resolve_template(message),
        from_email=message.contact_email,
        recipient_list=["secretary@mpga.net", ],
        context={
            "message": message,
            "logo_image": inline_image,
            "tournament": message.event
        },
        template_suffix="html",
        headers={"Reply-To": "no-reply@mpga.net"}
    )


def resolve_template(message):
    if message.message_type == "bid":
        return "tournament_bid.html"
    elif message.message_type == "tournament":
        return "tournament_message.html"
    elif message.message_type == "match-play":
        return "contact_message.html"
    else:
        return "contact_message.html"


def send_dues_confirmation(year, club):

    send_templated_mail(
        template_name="dues_confirmation.html",
        from_email="secretary@mpga.net",
        recipient_list=[cc.email for cc in club.contacts.all() if cc.email],
        context={
            "logo_image": inline_image,
            "year": year,
            "club_name": club.name
        },
        template_suffix="html",
        headers={"Reply-To": "no-reply@mpga.net"}
    )


class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = djoser_settings.ACTIVATION_URL.format(**context)
        context["logo_image"] = inline_image
        return context
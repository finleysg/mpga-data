import os
from django.conf import settings
from templated_email import send_templated_mail
from templated_email import InlineImage

# logo_file = os.path.join(settings.BASE_DIR, 'templates/templated_email/logo.png')
# with open(logo_file, 'rb') as logo:
#     image = logo.read()
#     inline_image = InlineImage(filename=logo_file, content=image)


def forward_contact_message(message):

    send_templated_mail(
        template_name=resolve_template(message.message_type),
        from_email=message.contact_email,
        recipient_list=resolve_to_list(message.message_type),
        # context={
        #     "message": message,
        #     'admin_url': '{}/admin/communication/contact/?q={}'.format(admin_url, message.id),  # TODO
        #     'logo_image': inline_image
        # },
        template_suffix='html',
        headers={"Reply-To": "no-reply@mpga.net"}
    )


def resolve_template(message_type):
    # Message types: bid, tournament, match play, general
    return ""


def resolve_to_list(message_type):
    return []

import json
import logging

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
webhook_secret = settings.STRIPE_WEBHOOK_SECRET
logger = logging.getLogger(__name__)


def get_payment_intent(amount_due, club, user_email):
    return stripe.PaymentIntent.create(
        amount=amount_due,
        currency='usd',
        automatic_payment_methods={"enabled": True},
        description='Club dues for ' + club.name,
        metadata={
            'club_id': str(club.id),
            'club_name': club.name,
            'user_email': user_email,
        },
        receipt_email=user_email,
    )


def unpack_stripe_event(request):
    try:
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        logger.error("Failed to unpack the json response from Stripe.")
        logger.error(e)
        return None

    return event

# def stripe_charge(user, token, description, amount_due, **kwargs):
#     return stripe.Charge.create(
#         amount=amount_due,
#         currency="usd",
#         source=token,
#         receipt_email=user.email,
#         description=description,
#         metadata=kwargs
#     )

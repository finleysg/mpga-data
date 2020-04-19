import json
import logging

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


def get_payment_intent(amount_due, club):
    return stripe.PaymentIntent.create(
        amount=amount_due,
        currency='usd',
        description='Club dues for ' + club.name,
        metadata={
            'payment_type': 'club_dues',
            'club_id': str(club.id),
            'club_name': club.name,
        },
    )


def unpack_stripe_event(payload):
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
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

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def stripe_charge(user, token, description, amount_due, **kwargs):
    return stripe.Charge.create(
        amount=amount_due,
        currency="usd",
        source=token,
        receipt_email=user.email,
        description=description,
        metadata=kwargs
    )

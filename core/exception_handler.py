import logging

from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback

from core.views import is_localhost

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    # to get the standard error response.
    response = exception_handler(exc, context)
    if 'request' in context:
        logger.error(exc, extra={'request': context['request']})
    else:
        logger.error(exc, extra={'context': context})

    # response == None is an exception not handled by the DRF framework in the call above
    if response is None:
        response = Response({'detail': 'Internal server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exc, OSError):
        pass
    elif isinstance(exc, NotAuthenticated):
        pass
    elif isinstance(exc, NotFound):
        pass
    else:
        logger.error(exc, exc_info=True)

    if len(exc.args) > 0 and exc.args[0] == "Invalid token.":
        logger.warning("Detected an invalid token: deleting cookie")
        response.delete_cookie(
            key = "mpga_access_token",
            path = "/",
            samesite = "Lax",
            domain = "data.mpga.net" if not is_localhost else None,
        )

    return response

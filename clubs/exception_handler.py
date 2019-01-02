import logging

from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

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

    return response

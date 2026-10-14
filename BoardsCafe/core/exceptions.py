import logging
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            'success': False,
            'message': 'An error occurred.',
            'errors': response.data,
        }

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response['message'] = 'Authentication credentials were not provided or are invalid.'
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response['message'] = 'You do not have permission to perform this action.'
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response['message'] = 'The requested resource was not found.'
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response['message'] = 'Validation failed.'
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            custom_response['message'] = 'Rate limit exceeded. Please try again later.'
        elif response.status_code >= 500:
            custom_response['message'] = 'An internal server error occurred.'
            custom_response['errors'] = {}
            logger.error(f'Server error: {exc}', exc_info=True)

        response.data = custom_response
    else:
        logger.error(f'Unhandled exception: {exc}', exc_info=True)
        return Response({
            'success': False,
            'message': 'An internal server error occurred.',
            'errors': {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


class APIException(Exception):
    def __init__(self, message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.errors = errors or {}
        self.status_code = status_code
        super().__init__(message)
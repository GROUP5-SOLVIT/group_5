from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message='Operation completed successfully.', status_code=status.HTTP_200_OK):
    response_data = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response_data['data'] = data
    return Response(response_data, status=status_code)


def error_response(message='Something went wrong.', errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    response_data = {
        'success': False,
        'message': message,
    }
    if errors is not None:
        response_data['errors'] = errors
    return Response(response_data, status=status_code)


def created_response(data=None, message='Resource created successfully.'):
    return success_response(data, message, status.HTTP_201_CREATED)


def no_content_response(message='Operation completed successfully.'):
    return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging

logger=logging.getLogger(__name__)

def custom_exception_handler(exc,context):
    response = exception_handler(exc,context)

    if response is not None:
        custom_response_data={
            'success':False,
            'error':{
                'status_code':response.status_code,
                'message':get_error_message(response.status_code,exc),
                'details':response.data,
                'type':exc.__class__.__name__
            }
        }
        response.data=custom_response_data

        logger.error(f"Error {response.status_code}: {exc}", exc_info=True)
    
    else:
        
        custom_response_data = {
            'success': False,
            'error': {
                'status_code': 500,
                'message': 'An unexpected error occurred',
                'details': str(exc) if settings.DEBUG else 'Internal server error',
                'type': exc.__class__.__name__
            }
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.exception(f"Unexpected error: {exc}")

    return response

def get_error_message(status_code, exc):

    messages = {
        400: 'Invalid request data',
        401: 'Authentication required',
        403: 'Permission denied',
        404: 'Resource not found',
        405: 'Method not allowed',
        429: 'Too many requests',
        500: 'Internal server error',
    }
    return messages.get(status_code, 'An error occurred')
   
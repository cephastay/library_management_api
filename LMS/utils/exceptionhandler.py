from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def customexceptionhandler(exc, context):
    """
    Custom exception handler for handling specific exceptions and returning appropriate responses.
    """
    # Define handlers for specific exceptions
    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error,
        'PermissionDenied': _handle_generic_error,
        'NotAuthenticated': _handle_authentication_error,
        'ValueError': _handle_generic_error,
        'IntegrityError': _handle_generic_error,
    }

    # Get the standard DRF response
    response = exception_handler(exc, context)

    # Get the exception class name
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # Use the appropriate handler for the exception
        return handlers[exception_class](exc, context, response)

    # Handle unhandled exceptions with a generic error
    return _handle_unhandled_error(exc, context, response)


def _handle_generic_error(exc, context, response):
    """
    Generic handler for exceptions like ValidationError, Http404, etc.
    """
    if response is not None:
        response.data = {
            "error": exc.detail if hasattr(exc, 'detail') else str(exc),
            "status_code": response.status_code
        }
    return response


def _handle_authentication_error(exc, context, response):
    """
    Handler for authentication-related exceptions.
    """
    if response is not None:
        response.data = {
            "error": "Log in to proceed",
            "status_code": status.HTTP_401_UNAUTHORIZED  # Explicit status code for unauthorized access
        }
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return response


def _handle_unhandled_error(exc, context, response):
    """
    Generic handler for unhandled exceptions.
    """
    if response is not None:
        response.data = {
            "error": "An unexpected error occurred. Please try again later.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR  # Generic 500 error for unknown issues
        }
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return response

import logging
from django.http import HttpResponseServerError, HttpResponseForbidden
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
import datetime
from dateutil import parser

logger = logging.getLogger(__name__)

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # Handle other exceptions
            pass

    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            return HttpResponseForbidden(render_to_string('core/403.html', request=request))
        # Log the exception
        logger.error(f"500 error occurred: {str(exception)}", exc_info=True)
        
        try:
            # Handle all exceptions with 500 error
            context = {'error_message': str(exception)}
            return HttpResponseServerError(
                render_to_string('core/500.html', context, request)
            )
        except Exception as e:
            # Fallback error handling if template rendering fails
            logger.error(f"Error in exception middleware: {str(e)}", exc_info=True)
            return HttpResponseServerError("Internal Server Error", content_type="text/plain")

import os
from django.http import HttpResponseForbidden

class HeaderCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin') or request.path.startswith('/static') or "add-to-group" in request.path:
            response = self.get_response(request)
            return response

        required_header = 'Authorizations'
        if request.headers.get(required_header) != os.environ.get('API_TOKEN'):
            return HttpResponseForbidden("Forbidden: Missing or incorrect header value.")

        response = self.get_response(request)
        return response

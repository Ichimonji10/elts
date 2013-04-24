from django.core import urlresolvers
from django import http

def index(request):
    """Redirect user to ELTS application."""
    return http.HttpResponseRedirect(urlresolvers.reverse('elts.views.index'))

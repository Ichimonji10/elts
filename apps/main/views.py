"""Business logic for all URLs in the ``main`` application.

For details on what each function is responsible for, see ``main/urls.py``.
That module documents both URL-to-function mappings and the exact
responsiblities of each function.

"""
from django.core import urlresolvers
from django import http

def index(request): # pylint: disable=W0613
    """Redirect user to ELTS application."""
    return http.HttpResponseRedirect(urlresolvers.reverse('elts.views.index'))

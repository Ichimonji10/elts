"""This module implements business logic for all URIs in the application.

Each function in this module is typically responsible for requests to a single
URI, including any arguments. For example, ``item()`` is responsible for
requests to the URIs ``item/`` and ``item/?tag=laptop``, but not ``item/15/``.

For more details on what each function is responsible for, see ``elts/urls.py``.
That module documents both URI-to-function mappings and the exact
responsiblities of each function.

"""
from django import http, template
from django.core import urlresolvers
from elts.models import Item, Reservation, Lend, Tag

def index(request):
    """Returns a summary of information about ELTS."""
    tplate = template.loader.get_template('elts/index.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))

def calendar(request):
    """Returns a calendar displaying reservations and lends."""
    tplate = template.loader.get_template('elts/calendar.html')
    ctext = template.RequestContext(
        request,
        {}
    )
    return http.HttpResponse(tplate.render(ctext))

def item(request):
    """Either shows all items or creates a new item."""
    if 'GET' == request.method:
        # Return a list of all items.
        tplate = template.loader.get_template('elts/item-read.html')
        ctext = template.RequestContext(
            request,
            {'items': Item.objects.all()}
        )
        return http.HttpResponse(tplate.render(ctext))

    elif 'POST' == request.method:
        # Fetch and validate arguments. TODO: improve validation
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        errors = []
        if not name:
            errors.append('No name was given.')

        if errors:
            # Send user back to form so they can correct their mistakes and
            # re-submit it.
            request.session['errors'] = errors
            request.session['name'] = name
            request.session['description'] = description
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.item_create_form')
            )
        else:
            # Create an ``Item`` and redirect the user to an appropriate page.
            Item(name = name, description = description).save()
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.item')
            )

    else:
        # The HTTP request ain't a GET or POST, so ignore the request.
        pass

def item_create_form(request):
    """Returns a form for creating a new item."""
    tplate = template.loader.get_template('elts/item-create.html')
    ctext = template.RequestContext(
        request,
        {
            'errors': request.session.pop('errors', []),
            'name': request.session.pop('name', ''),
            'description': request.session.pop('description', ''),
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def reservation(request):
    tplate = template.loader.get_template('elts/reservation.html')
    ctext = template.RequestContext(
        request,
        {
            'reservations': Reservation.objects.all()
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def lend(request):
    tplate = template.loader.get_template('elts/lend.html')
    ctext = template.RequestContext(
        request,
        {
            'lends': Lend.objects.all()
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def tag(request):
    tplate = template.loader.get_template('elts/tag.html')
    ctext = template.RequestContext(
        request,
        {
            'tags': Tag.objects.all()
        }
    )
    return http.HttpResponse(tplate.render(ctext))

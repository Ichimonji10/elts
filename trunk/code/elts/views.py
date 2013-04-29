"""Business logic for all URLs in the ``elts`` application.

For details on what each function is responsible for, see ``elts/urls.py``.
That module documents both URL-to-function mappings and the exact
responsiblities of each function.

Naming Conventions
==================

Each function in this module is responsible for all requests to a single URL,
including any arguments. For example, ``item()`` is responsible for requests to
the URLs ``item/`` and ``item/?tag=laptop``, but not ``item/15/``. Each function
is typically named after the URL it handles. So, ``item/create-form/`` is
handled by ``item_create_form()``.

This naming convention holds true not only for function names, but also template
names, except that where functions use underscores, templates use dashes.  For
example, ``item_create_form()`` uses the template ``item-create-form.html``.

Several function arguments are named with a trailing underscore. For example,
``item_id()`` takes an argument called ``item_id_``. This is done to avoid name
clashes, and is in accordance with PEP 8. See details `here
<http://www.python.org/dev/peps/pep-0008/#function-and-method-arguments>`_.

Other Notes
===========

Pylint error 1101 is ignored at several places in this file. The error typically
reads "Class 'Item' has no 'objects' member".

"""
from django.core import urlresolvers
from django import http, template
from elts import models

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
        tplate = template.loader.get_template('elts/item.html')
        ctext = template.RequestContext(
            # pylint: disable=E1101
            request,
            {'items': models.Item.objects.all()}
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
            models.Item(name = name, description = description).save()
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.item')
            )

    else:
        # The HTTP request ain't a GET or POST, so ignore the request.
        pass

def item_create_form(request):
    """Returns a form for creating a new item."""
    tplate = template.loader.get_template('elts/item-create-form.html')
    ctext = template.RequestContext(
        request,
        {
            'errors': request.session.pop('errors', []),
            'name': request.session.pop('name', ''),
            'description': request.session.pop('description', ''),
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def item_id(request, item_id_):
    """Returns information about a specific item."""
    tplate = template.loader.get_template('elts/item-id.html')
    ctext = template.RequestContext(
        request,
        {
            # pylint: disable=E1101
            'item_id': item_id_,
            'item': models.Item.objects.filter(id = item_id_)[0],
#            'item_tags': models.Tag.objects.filter(
#                id__in = models.ItemTag.objects.filter(item_id = item_id_)
#            )
        }
    )
    return http.HttpResponse(tplate.render(ctext))

def item_id_update_form(request, item_id_):
    """Returns a form for updating the item with id ``item_id_``."""
    # pylint: disable=E1101
    item_ = models.Item.objects.filter(id = item_id_)[0]
    if item_:
        tplate = template.loader.get_template('elts/item-id-update-form.html')
        ctext = template.RequestContext(
            request,
            {
                'item': models.Item.objects.filter(id = item_id_)[0],
            }
        )
        return http.HttpResponse(tplate.render(ctext))
    else:
        return http.HttpResponseRedirect(
            urlresolvers.reverse('elts.views.item_id'),
            item_id = item_id_,
        )

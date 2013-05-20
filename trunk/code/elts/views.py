"""Business logic for all URLs in the ``elts`` application.

For details on what each function is responsible for, see ``elts/urls.py``.
That module documents both URL-to-function mappings and the exact
responsiblities of each function.

Naming Conventions
==================

Functions
---------

Each function in this module is responsible for all requests to a single URL,
including any arguments. For example, ``item()`` is responsible for requests to
the URLs ``item/`` and ``item/?tag=laptop``, but not ``item/15/``. Each function
is typically named after the URL it handles. So, ``item/create-form/`` is
handled by ``item_create_form()``.

Several function arguments are named with a trailing underscore. For example,
``item_id()`` takes an argument called ``item_id_``. This is done to avoid name
clashes, and is in accordance with PEP 8. See details `here
<http://www.python.org/dev/peps/pep-0008/#function-and-method-arguments>`_.

Templates
---------

This naming convention holds true not only for function names, but also template
names, except that where functions use underscores, templates use dashes.  For
example, ``item_create_form()`` uses the template ``item-create-form.html``.

Subtemplates are named with a leading underscore. This is in accordance with the
Ruby on Rails community convention. A quick reminder: a subtemplate is just a
normal template that is intended to be included in other templates with an
``include`` tag. For example::

    {% include 'elts/_item-edit-form.html' %}

Other Notes
===========

Pylint error 1101 is ignored at several places in this file. The error typically
reads "Class 'Item' has no 'objects' member".

"""
from django.core import urlresolvers
from django import http, shortcuts, template
from elts import models
from elts import forms

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
    # Return a list of all items.
    if 'GET' == request.method:
        return shortcuts.render(
            # pylint: disable=E1101
            # Class 'Item' has no 'objects' member
            request,
            'elts/item.html',
            {'items': models.Item.objects.all()}
        )

    # Create a new item.
    elif 'POST' == request.method:
        # pylint: disable=E1101
        # Instance of 'ItemForm' has no 'is_valid' member
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            models.Item(
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
            ).save()
            return http.HttpResponseRedirect(
                # TODO: redirect to specific item page?
                # TODO: test form validation and data redisplay
                urlresolvers.reverse('elts.views.item')
            )
        else:
            # Put ``form`` into session for retreival by ``item_create_form``.
            request.session['form'] = form
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.item_create_form')
            )

    # The HTTP request ain't a GET or POST, so ignore the request.
    else:
        pass

def item_create_form(request):
    """Returns a form for creating a new item."""
    return shortcuts.render(
        request,
        'elts/item-create-form.html',
        {
            # If user submits a form containing errors, method ``item`` will put
            # that form into session storage. Use it if available.
            'form': request.session.pop('form', forms.ItemForm())
        }
    )

def item_id(request, item_id_):
    """Returns information about a specific item."""
    return shortcuts.render(
        request,
        'elts/item-id.html',
        {
            # pylint: disable=E1101
            # Class 'Item' has no 'objects' member
            'item_id': item_id_,
            'item': models.Item.objects.filter(id = item_id_)[0],
        }
    )
    # 'item_tags': models.Tag.objects.filter(
    #     id__in = models.ItemTag.objects.filter(item_id = item_id_)
    # )

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

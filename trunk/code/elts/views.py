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

Pylint error 1101 is ignored at several places in this file. Examples of this
error include:

    Class 'Item' has no 'objects' member
    Instance of 'ItemForm' has no 'is_valid' member
    Instance of 'ItemForm' has no 'cleaned_data' member
    Instance of 'TagForm' has no 'is_valid' member
    Instance of 'TagForm' has no 'cleaned_data' member

"""
from django.core import urlresolvers
from django import http, shortcuts
from elts import forms
from elts import models

def index(request):
    """Returns a summary of information about ELTS."""
    return shortcuts.render(request, 'elts/index.html', {})

def calendar(request):
    """Returns an HTML calendar displaying reservations and lends."""
    return shortcuts.render(request, 'elts/calendar.html', {})

def item(request):
    """Returns information about all items or creates a new item."""
    # Return a list of all items.
    if 'GET' == request.method:
        return shortcuts.render(
            # pylint: disable=E1101
            request,
            'elts/item.html',
            {'items': models.Item.objects.all()}
        )

    # Create a new item.
    elif 'POST' == request.method:
        # pylint: disable=E1101
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save()
            return http.HttpResponseRedirect(
                urlresolvers.reverse(
                    'elts.views.item_id',
                    args = [new_item.id]
                )
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
    """Read, update, or delete item ``item_id_``."""
    # pylint: disable=E1101
    item_ = models.Item.objects.get(id = item_id_)
    if 'GET' == request.method:
        return shortcuts.render(
            request,
            'elts/item-id.html',
            {
                'item': item_,
                'form': request.session.pop('form', forms.ItemNoteForm()),
            }
        )

    elif 'POST' == request.method \
    and  'PUT'  == request.POST.get('method_override', False):
        form = forms.ItemForm(request.POST, instance = item_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.item_id', args = [item_id_])
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                urlresolvers.reverse(
                    'elts.views.item_id_update_form',
                    args = [item_id_]
                )
            )

    elif 'POST'   == request.method \
    and  'DELETE' == request.POST.get('method_override', False):
        try:
            models.Item.objects.get(id = item_id_).delete()
        except AttributeError:
            pass
        return http.HttpResponseRedirect(
            urlresolvers.reverse('elts.views.item')
        )

    else:
        pass

def item_id_update_form(request, item_id_):
    """Returns a form for updating item ``item_id_``.

    The form is pre-populated with existing data about item ``item_id_``.

    """
    # pylint: disable=E1101
    item_ = models.Item.objects.get(id = item_id_)
    return shortcuts.render(
        request,
        'elts/item-id-update-form.html',
        {
            'item': item_,
            'form': request.session.pop(
                'form',
                forms.ItemForm(instance = item_)
            ),
        }
    )

def item_id_delete_form(request, item_id_):
    """Returns a form for deleting item ``item_id_``."""
    return shortcuts.render(
        # pylint: disable=E1101
        request,
        'elts/item-id-delete-form.html',
        {'item': models.Item.objects.get(id = item_id_)}
    )

def tag(request):
    """Returns information about all tags or creates a new tag."""
    # Return a list of all tags.
    if 'GET' == request.method:
        return shortcuts.render(
            # pylint: disable=E1101
            request,
            'elts/tag.html',
            {'tags': models.Tag.objects.all()}
        )

    # Create a new tag.
    elif 'POST' == request.method:
        # pylint: disable=E1101
        form = forms.TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return http.HttpResponseRedirect(
                urlresolvers.reverse(
                    'elts.views.tag_id',
                    args = [new_tag.id],
                )
            )
        else:
            # Put ``form`` into session for retreival by ``tag_create_form``.
            request.session['form'] = form
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.tag_create_form')
            )

    # The HTTP request ain't a GET or POST, so ignore the request.
    else:
        pass

def tag_id(request, tag_id_):
    """Read, update, or delete tag ``tag_id_``."""
    # pylint: disable=E1101
    tag_ = models.Tag.objects.get(id = tag_id_)
    if 'GET' == request.method:
        return shortcuts.render(request, 'elts/tag-id.html', {'tag': tag_})

    elif 'POST' == request.method \
    and  'PUT'  == request.POST.get('method_override', False):
        form = forms.TagForm(request.POST, instance = tag_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.tag_id', args = [tag_id_])
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                urlresolvers.reverse(
                    'elts.views.tag_id_update_form',
                    args = [tag_id_]
                )
            )

    elif 'POST'   == request.method \
    and  'DELETE' == request.POST.get('method_override', False):
        try:
            models.Tag.objects.get(id = tag_id_).delete()
        except AttributeError:
            pass
        return http.HttpResponseRedirect(
            urlresolvers.reverse('elts.views.tag')
        )

    else:
        pass

def tag_create_form(request):
    """Returns a form for creating a new tag."""
    return shortcuts.render(
        request,
        'elts/tag-create-form.html',
        {
            # Put ``form`` into session for retreival by ``tag_create_form``.
            'form': request.session.pop('form', forms.TagForm())
        }
    )

def tag_id_update_form(request, tag_id_):
    """Returns a form for updating tag ``tag_id_``.

    The form is pre-populated with existing data about tag ``tag_id_``.

    """
    # pylint: disable=E1101
    tag_ = models.Tag.objects.get(id = tag_id_)
    return shortcuts.render(
        request,
        'elts/tag-id-update-form.html',
        {
            'tag': tag_,
            'form': request.session.pop('form', forms.TagForm(instance = tag_)),
        }
    )

def tag_id_delete_form(request, tag_id_):
    """Returns a form for updating tag ``tag_id_``."""
    return shortcuts.render(
        # pylint: disable=E1101
        request,
        'elts/tag-id-delete-form.html',
        {'tag': models.Tag.objects.get(id = tag_id_)}
    )

def item_note(request):
    """Creates a new item note."""
    if 'POST' == request.method:
        # For which item is this note being created?
        try:
            item_ = models.Item.objects.get(
                id = request.POST.get('item_id', None)
            )
        except models.Item.DoesNotExist:
            return http.HttpResponseRedirect(
                urlresolvers.reverse('elts.views.item')
            )

        # Get note text and, if valid, save the note.
        form = forms.ItemNoteForm(request.POST)
        if form.is_valid():
            models.ItemNote(
                note_text = form.cleaned_data['note_text'],
                #author_id = None, # FIXME
                item_id = item_,
            ).save()
        else:
            request.session['form'] = form

        # Return the user to this page whether or not the note was saved.
        return http.HttpResponseRedirect(
            urlresolvers.reverse('elts.views.item_id', args = [item_.id])
        )

    else:
        pass

def item_note_id(request, item_note_id_):
    """Updates or deletes item note ``item_note_id_``."""
    if 'POST' == request.method \
    and 'PUT'  == request.POST.get('method_override', False):
        item_note_ = models.ItemNote.objects.get(id = item_note_id_)
        form = forms.ItemNoteForm(request.POST, instance = item_note_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                urlresolvers.reverse(
                    'elts.views.item_note_id',
                    args = [item_note_id_]
                )
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                urlresolvers.reverse(
                    'elts.views.item_note_id_update_form',
                    args = [item_note_id_]
                )
            )

    elif 'POST' == request.method \
    and  'DELETE'  == request.POST.get('method_override', False):
        try:
            models.ItemNote.objects.get(id = item_note_id_).delete()
        except AttributeError:
            pass
        # FIXME: return to specific item's page
        return http.HttpResponseRedirect(
            urlresolvers.reverse('elts.views.item')
        )

    else:
        pass

def item_note_id_update_form(request, item_note_id_):
    """Returns a form for updating item note ``item_note_id_``.

    The form is pre-populated with existing data about item note
    ``item_note_id_``.

    """
    item_note_ = models.ItemNote.objects.get(id = item_note_id_)
    return shortcuts.render(
        request,
        'elts/item-note-id-update-form.html',
        {
            'item_note': item_note_,
            'form': request.session.pop(
                'form',
                forms.ItemNoteForm(instance = item_note_)
            ),
        }
    )

def item_note_id_delete_form(request, item_note_id_):
    """Returns a form for deleting item note ``item_note_id_``."""
    return shortcuts.render(
        request,
        'elts/item-note-id-delete-form.html',
        {'item_note': models.ItemNote.objects.get(id = item_note_id_)}
    )

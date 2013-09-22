"""Business logic for all URLs in the ``elts`` application.

To see what HTTP operations each URL accepts, see ``elts/urls.py``.

Naming Conventions
==================

Functions
---------

Each function in this module is responsible for all requests to a single URL,
including any arguments. For example, ``item()`` is responsible for the requests
``GET item/`` and ``GET item/?tag=laptop/``, but not ``GET item/15/``. Each
function is typically named after the URL it handles. So, ``item/create-form/``
is handled by ``item_create_form()``, and ``item/15/update-form/`` is handled by
``item_id_update_form()``.

Several function arguments use a trailing underscore in their name. For example,
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

"""
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django import http
from django.shortcuts import render
from elts import forms
from elts import models
from calendar import Calendar, day_name
from datetime import date

# pylint: disable=E1101
# Instance of 'ItemForm' has no 'is_valid' member (no-member)
# Instance of 'ItemForm' has no 'save' member (no-member)
# Class 'Item' has no 'objects' member (no-member)

@login_required
def index(request):
    """Handle a request for ``/``."""
    def get_handler():
        """Return a summary of information about ELTS."""
        return render(request, 'elts/index.html', {})

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def calendar(request):
    """Handle a request for ``calendar/``."""
    def get_handler():
        """Show items going out and coming back this month."""
        # TODO: allow users to decide which day starts the week.
        return render(
            request,
            'elts/calendar.html',
            {
                'today': date.today(),
                'day_names': [
                    day_name[day_num]
                    for day_num
                    in Calendar().iterweekdays()
                ]
            }
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item(request):
    """Handle a request for ``item/``."""
    def post_handler():
        """Create a new item.

        If creation succeeds, redirect user to ``item_id`` view. Otherwise,
        redirect user to ``item_create_form`` view.

        """
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save()
            return http.HttpResponseRedirect(
                reverse('elts.views.item_id', args = [new_item.id])
            )
        else:
            # Put ``form`` into session for retreival by ``item_create_form``.
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse('elts.views.item_create_form')
            )

    def get_handler():
        """Return a list of all items."""
        return render(
            request,
            'elts/item.html',
            {'items': models.Item.objects.all()}
        )

    return {
        'POST': post_handler,
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_create_form(request):
    """Handle a request for ``item/create-form/``."""
    def get_handler():
        """Return a form for creating an item."""
        return render(
            request,
            'elts/item-create-form.html',
            # If user submits a form containing errors, method ``item`` will
            # put that form into session storage. Use it if available.
            {'form': request.session.pop('form', forms.ItemForm())}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_id(request, item_id_):
    """Handle a request for ``item/<id>/``."""
    try:
        item_ = models.Item.objects.get(id = item_id_)
    except models.Item.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return information about item ``item_id_``."""
        return render(
            request,
            'elts/item-id.html',
            {
                'item': item_,
                'form': request.session.pop('form', forms.ItemNoteForm()),
            }
        )

    def put_handler():
        """Update item ``item_id_``.

        If update succeeds, redirect user to ``item_id`` view. Otherwise,
        redirect user to ``item_id_update_form``.

        """
        form = forms.ItemForm(request.POST, instance = item_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                reverse('elts.views.item_id', args = [item_id_])
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse('elts.views.item_id_update_form', args = [item_id_])
            )

    def delete_handler():
        """Delete item ``item_id_``.

        After delete, redirect user to ``item`` view.

        """
        item_.delete()
        return http.HttpResponseRedirect(reverse('elts.views.item'))

    return {
        'GET': get_handler,
        'PUT': put_handler,
        'DELETE': delete_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_id_update_form(request, item_id_):
    """Handle a request for ``item/<id>/update-form/``."""
    try:
        item_ = models.Item.objects.get(id = item_id_)
    except models.Item.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for updating item ``item_id_``."""
        form = request.session.pop('form', forms.ItemForm(instance = item_))
        return render(
            request,
            'elts/item-id-update-form.html',
            {'item': item_, 'form': form}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_id_delete_form(request, item_id_):
    """Handle a request for ``item/<id>/delete-form/``."""
    try:
        item_ = models.Item.objects.get(id = item_id_)
    except models.Item.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for deleting item ``item_id_``."""
        return render(request, 'elts/item-id-delete-form.html', {'item': item_})

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def tag(request):
    """Handle a request for ``tag/``."""
    def post_handler():
        """Create a tag.

        If creation succeeds, redirect user to ``tag_id`` view. Otherwise,
        redirect user to ``tag_create_form`` view.

        """
        form = forms.TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return http.HttpResponseRedirect(
                reverse(
                    'elts.views.tag_id',
                    args = [new_tag.id],
                )
            )
        else:
            # Put ``form`` into session for retreival by ``tag_create_form``.
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse('elts.views.tag_create_form')
            )

    def get_handler():
        """Return information about all tags."""
        return render(
            request,
            'elts/tag.html',
            {'tags': models.Tag.objects.all()}
        )

    return {
        'POST': post_handler,
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def tag_id(request, tag_id_):
    """Handle a request for ``tag/<id>/``."""
    try:
        tag_ = models.Tag.objects.get(id = tag_id_)
    except models.Tag.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return information about tag ``tag_id_``."""
        return render(request, 'elts/tag-id.html', {'tag': tag_})

    def put_handler():
        """Update tag ``tag_id_``.

        If update succeeds, redirect user to ``tag_id`` view. Otherwise,
        redirect user to ``update_form`` view.

        """
        form = forms.TagForm(request.POST, instance = tag_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                reverse('elts.views.tag_id', args = [tag_id_])
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse(
                    'elts.views.tag_id_update_form',
                    args = [tag_id_]
                )
            )

    def delete_handler():
        """Delete tag ``tag_id_``.

        After deletion, redirect user to ``tag`` view.

        """
        tag_.delete()
        return http.HttpResponseRedirect(reverse('elts.views.tag'))

    return {
        'GET': get_handler,
        'PUT': put_handler,
        'DELETE': delete_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def tag_create_form(request):
    """Handle a request for ``tag/create-form/``."""
    def get_handler():
        """Return a form for creating a new tag."""
        return render(
            request,
            'elts/tag-create-form.html',
            {
                # Put ``form`` into session for retreival by ``tag_create_form``
                'form': request.session.pop('form', forms.TagForm())
            }
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def tag_id_update_form(request, tag_id_):
    """Handle a request for ``tag/<id>/update-form/``."""
    try:
        tag_ = models.Tag.objects.get(id = tag_id_)
    except models.Tag.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for updating tag ``tag_id_``."""
        return render(
            request,
            'elts/tag-id-update-form.html',
            {
                'tag': tag_,
                'form': request.session.pop(
                    'form',
                    forms.TagForm(instance = tag_)
                ),
            }
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def tag_id_delete_form(request, tag_id_):
    """Handle a request for ``tag/<id>/delete-form/``."""
    try:
        tag_ = models.Tag.objects.get(id = tag_id_)
    except models.Tag.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for updating tag ``tag_id_``."""
        return render(request, 'elts/tag-id-delete-form.html', {'tag': tag_})

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_note(request):
    """Handle a request for ``item-note/``."""
    def post_handler():
        """Create a new item note.

        Redirect user to ``item_id`` view after handling request.

        """
        # For which item is this note being created?
        try:
            item_ = models.Item.objects.get(
                id = request.POST.get('item_id', None)
            )
        except models.Item.DoesNotExist:
            return http.HttpResponse(status = 422)

        # Get note text and, if valid, save the note.
        form = forms.ItemNoteForm(request.POST)
        if form.is_valid():
            models.ItemNote(
                note_text = form.cleaned_data['note_text'],
                author_id = request.user,
                item_id = item_,
            ).save()
        else:
            request.session['form'] = form

        # Return the user to this page whether or not the note was saved.
        return http.HttpResponseRedirect(
            reverse('elts.views.item_id', args = [item_.id])
        )

    return {
        'POST': post_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_note_id(request, item_note_id_):
    """Handle a request for ``item-note/<id>/``."""
    try:
        item_note_ = models.ItemNote.objects.get(id = item_note_id_)
    except models.ItemNote.DoesNotExist:
        raise http.Http404
    item_id_ = item_note_.item_id.id

    def put_handler():
        """Update item note ``item_note_id_``.

        If update succeeds, redirect user to ``item_id`` view. Otherwise,
        redirect user to ``item_note_id_update_form`` view.

        """
        form = forms.ItemNoteForm(request.POST, instance = item_note_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                reverse(
                    'elts.views.item_id',
                    args = [item_id_]
                )
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse(
                    'elts.views.item_note_id_update_form',
                    args = [item_note_id_]
                )
            )

    def delete_handler():
        """Delete item note ``item_note_id_``.

        After deletion, redirect user to ``item_id`` view.

        """
        item_note_.delete()
        return http.HttpResponseRedirect(
            reverse('elts.views.item_id', args = [item_id_])
        )

    return {
        'PUT': put_handler,
        'DELETE': delete_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_note_id_update_form(request, item_note_id_):
    """Handle a request for ``item-note/<id>/update-form/``."""
    try:
        item_note_ = models.ItemNote.objects.get(id = item_note_id_)
    except models.ItemNote.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for updating item note ``item_note_id_``."""
        form = request.session.pop(
            'form',
            forms.ItemNoteForm(instance = item_note_)
        )
        return render(
            request,
            'elts/item-note-id-update-form.html',
            {'item_note': item_note_, 'form': form}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def item_note_id_delete_form(request, item_note_id_):
    """Handle a request for ``item-note/<id>/delete-form/``."""
    try:
        item_note_ = models.ItemNote.objects.get(id = item_note_id_)
    except models.ItemNote.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for deleting item note ``item_note_id_``."""
        return render(
            request,
            'elts/item-note-id-delete-form.html',
            {'item_note': item_note_}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend(request):
    """Handle a request for ``lend/``."""
    def post_handler():
        """Create a new item lend.

        If creation suceeds, redirect user to ``user_id`` view. Otherwise,
        redirect user to ``lend_create_form``.

        """
        form = forms.LendForm(request.POST)
        if form.is_valid():
            new_lend = form.save()
            return http.HttpResponseRedirect(
                reverse(
                    'elts.views.lend_id',
                    args = [new_lend.id],
                )
            )
        else:
            # Put ``form`` into session for retrieval by ``lend_create_form``.
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse('elts.views.lend_create_form')
            )

    def get_handler():
        """Return information about all lends."""
        return render(
            request,
            'elts/lend.html',
            {'lends': models.Lend.objects.all()}
        )

    return {
        'POST': post_handler,
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_create_form(request):
    """Handle a request for ``lend/create_form/``."""
    def get_handler():
        """Return a form for creating an lend."""
        return render(
            request,
            'elts/lend-create-form.html',
            # If user submits a form containing errors, method ``lend`` will
            # put that form into the session. Use it if available.
            {'form': request.session.pop('form', forms.LendForm())}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_id(request, lend_id_):
    """Handle a request for ``lend/<id>/``."""
    try:
        lend_ = models.Lend.objects.get(id = lend_id_)
    except models.Lend.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return information about lend ``lend_id_``."""
        return render(
            request,
            'elts/lend-id.html',
            {
                'lend': lend_,
                'form': request.session.pop('form', forms.LendNoteForm()),
            }
        )

    def put_handler():
        """Update lend ``lend_id_``.

        If update succeeds, redirect user to ``lend_id`` view. Otherwise,
        redirect user to ``lend_id_update_form``.

        """
        form = forms.LendForm(request.POST, instance = lend_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                reverse('elts.views.lend_id', args = [lend_id_])
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse('elts.views.lend_id_update_form', args = [lend_id_])
            )

    def delete_handler():
        """Delete lend ``lend_id_``.

        After delete, redirect user to ``lend`` view.

        """
        lend_.delete()
        return http.HttpResponseRedirect(reverse('elts.views.lend'))

    return {
        'GET': get_handler,
        'PUT': put_handler,
        'DELETE': delete_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_id_update_form(request, lend_id_):
    """Handle a request for ``lend/<id>/update-form/``."""
    try:
        lend_ = models.Lend.objects.get(id = lend_id_)
    except models.Lend.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for updating lend ``lend_id_``."""
        form = request.session.pop('form', forms.LendForm(instance = lend_))
        return render(
            request,
            'elts/lend-id-update-form.html',
            {'lend': lend_, 'form': form}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_id_delete_form(request, lend_id_):
    """Handle a request for ``lend/<id>/delete-form/``."""
    try:
        lend_ = models.Lend.objects.get(id = lend_id_)
    except models.Lend.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for deleting lend ``lend_id_``."""
        return render(request, 'elts/lend-id-delete-form.html', {'lend': lend_})

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_note(request):
    """Handle a request for ``lend-note/``."""
    def post_handler():
        """Create a new lend note.

        Redirect user to ``lend_id`` view after handling request.

        """
        # For which lend is this note being created?
        try:
            lend_ = models.Lend.objects.get(
                id = request.POST.get('lend_id', None)
            )
        except models.Lend.DoesNotExist:
            return http.HttpResponse(status = 422)

        # Get note text and, if valid, save the note.
        form = forms.LendNoteForm(request.POST)
        if form.is_valid():
            models.LendNote(
                note_text = form.cleaned_data['note_text'],
                author_id = request.user,
                lend_id = lend_,
            ).save()
        else:
            request.session['form'] = form

        # Return the user to this page whether or not the note was saved.
        return http.HttpResponseRedirect(
            reverse('elts.views.lend_id', args = [lend_.id])
        )

    return {
        'POST': post_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_note_id(request, lend_note_id_):
    """Handle a request for ``lend-note/<id>/``."""
    try:
        lend_note_ = models.LendNote.objects.get(id = lend_note_id_)
    except models.LendNote.DoesNotExist:
        raise http.Http404
    lend_id_ = lend_note_.lend_id.id

    def put_handler():
        """Update lend note ``lend_note_id_``.

        If update succeeds, redirect user to ``lend_id`` view. Otherwise,
        redirect user to ``lend_note_id_update_form`` view.

        """
        form = forms.LendNoteForm(request.POST, instance = lend_note_)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(
                reverse(
                    'elts.views.lend_id',
                    args = [lend_id_]
                )
            )
        else:
            request.session['form'] = form
            return http.HttpResponseRedirect(
                reverse(
                    'elts.views.lend_note_id_update_form',
                    args = [lend_note_id_]
                )
            )

    def delete_handler():
        """Delete lend note ``lend_note_id_``.

        After deletion, redirect user to ``lend_id`` view.

        """
        lend_note_.delete()
        return http.HttpResponseRedirect(
            reverse('elts.views.lend_id', args = [lend_id_])
        )

    return {
        'PUT': put_handler,
        'DELETE': delete_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_note_id_update_form(request, lend_note_id_):
    """Handle a request for ``lend-note/<id>/update-form/``."""
    try:
        lend_note_ = models.LendNote.objects.get(id = lend_note_id_)
    except models.LendNote.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for updating lend note ``lend_note_id_``."""
        form = request.session.pop(
            'form',
            forms.LendNoteForm(instance = lend_note_)
        )
        return render(
            request,
            'elts/lend-note-id-update-form.html',
            {'lend_note': lend_note_, 'form': form}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

@login_required
def lend_note_id_delete_form(request, lend_note_id_):
    """Handle a request for ``lend-note/<id>/delete-form/``."""
    try:
        lend_note_ = models.LendNote.objects.get(id = lend_note_id_)
    except models.LendNote.DoesNotExist:
        raise http.Http404

    def get_handler():
        """Return a form for deleting lend note ``lend_note_id_``."""
        return render(
            request,
            'elts/lend-note-id-delete-form.html',
            {'lend_note': lend_note_}
        )

    return {
        'GET': get_handler,
    }.get(
        _request_type(request),
        _http_405
    )()

def login(request):
    """Handle a request for ``login/``."""
    def get_handler():
        """Return a form for logging in."""
        return render(
            request,
            'elts/login.html',
            {'form': request.session.pop('form', forms.LoginForm())}
        )

    # Log in user
    def post_handler():
        """Log in user.

        If login suceeds, redirect user to ``index`` view. Otherwise, redirect
        user to ``login`` view.

        """
        # Check validity of submitted data
        form = forms.LoginForm(request.POST)
        if not form.is_valid():
            request.session['form'] = form
            return http.HttpResponseRedirect(reverse('elts.views.login'))

        # Check for invalid credentials.
        user = auth.authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        if user is None:
            form._errors[NON_FIELD_ERRORS] = form.error_class([
                'Credentials are invalid.'
            ])
            request.session['form'] = form
            return http.HttpResponseRedirect(reverse('elts.views.login'))

        # Check for inactive user
        if not user.is_active:
            form._errors[NON_FIELD_ERRORS] = form.error_class([
                'Account is inactive.'
            ])
            request.session['form'] = form
            return http.HttpResponseRedirect(reverse('elts.views.login'))

        # Everything checks out. Let 'em in.
        auth.login(request, user)
        return http.HttpResponseRedirect(reverse('elts.views.index'))

    # Log out user
    def delete_handler():
        """Log out user.

        Redirect user to ``login`` after logging out user.

        """
        auth.logout(request)
        return http.HttpResponseRedirect(reverse('elts.views.login'))

    return {
        'POST': post_handler,
        'GET': get_handler,
        'DELETE': delete_handler
    }.get(
        _request_type(request),
        _http_405
    )()

def _request_type(request):
    """Determine what HTTP method ``request.method`` represents.

    ``request`` is a ``django.http.HttpRequest`` object.

    If ``request`` is an HTTP POST request and '_method' is a query string key,
    return the corresponding value. Otherwise, return ``request.method``.

    """
    method = request.method
    if 'POST' == method:
        return request.POST.get('_method', 'POST')
    return method

def _http_405():
    """Return an ``HttpResponse`` with a 405 status code."""
    return http.HttpResponse(status = 405)

"""Forms for creating and updating objects.

Unless otherwise noted, all forms defined herein can be used to either create or
update an object.

"""
from datetime import timedelta
from django.db.models import Q
from django.forms import CharField, Form, ModelForm, widgets, ValidationError
from elts import models

# pylint: disable=R0903
# "Too few public methods (0/2)"
# It is both common and OK for a model to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method"
# It is both common and OK for a model to have no __init__ method.

class ItemForm(ModelForm):
    """A form for an Item."""

    class Meta(object):
        """Form attributes that are not fields."""
        model = models.Item
        fields = ['name', 'description', 'tags', 'is_lendable']
        widgets = {'description': widgets.Textarea()}

class TagForm(ModelForm):
    """A form for a Tag."""

    class Meta(object):
        """Form attributes that are not fields."""
        model = models.Tag
        fields = ['name', 'description']
        widgets = {'description': widgets.Textarea()}

# Start `NoteForm` definitions.

class ItemNoteForm(ModelForm):
    """A form for a ItemNote."""

    class Meta(object):
        """Form attributes that are not fields."""
        model = models.ItemNote
        fields = ['note_text']
        widgets = {'note_text': widgets.Textarea()}

class UserNoteForm(ModelForm):
    """A form for a UserNote."""

    class Meta(object):
        """Form attributes that are not fields."""
        model = models.UserNote
        fields = ['note_text']
        widgets = {'note_text': widgets.Textarea()}

class LendNoteForm(ModelForm):
    """A form for a LendNote."""

    class Meta(object):
        """Form attributes that are not fields."""
        model = models.LendNote
        fields = ['is_complaint', 'note_text']
        widgets = {'note_text': widgets.Textarea()}

# End `NoteForm` definitions.

class LoginForm(Form):
    """A form for logging in a ``User``."""
    username = CharField()
    password = CharField(widget = widgets.PasswordInput)

    class Meta(object):
        """Form attributes that are not fields."""
        fields = ['username', 'password']

class LendForm(ModelForm):
    """A form for a Lend."""

    class Meta(object):
        """Form attributes that are not fields."""
        model = models.Lend
        fields = ['item_id', 'user_id', 'due_out', 'due_back', 'out', 'back']
        widgets = {
            'due_out':  widgets.DateInput(attrs = {'type': 'date'}),
            'due_back': widgets.DateInput(attrs = {'type': 'date'}),
            'out':  widgets.DateTimeInput(attrs = {'type': 'datetime'}),
            'back': widgets.DateTimeInput(attrs = {'type': 'datetime'}),
        }

    # FIXME: This is a whale of a function.
    # FIXME: Add unit tests.
    def clean(self):
        """Perform form-wide validation.

        This method is called after ``Field.clean()`` has been called on each
        individual field. "Any ValidationError raised by this method will
        not be associated with a particular field; it will have a special-case
        association with the field named '__all__'."

        """
        # Let the ``ModelForm`` parent class do some checks.
        cleaned_data = super(LendForm, self).clean()
        # Grab data necessary for validation.
        item_id = cleaned_data.get('item_id')
        due_out = cleaned_data.get('due_out')
        due_back = cleaned_data.get('due_back')
        out = cleaned_data.get('out')
        back = cleaned_data.get('back')

        # Either ``due_out`` or ``out`` must be set.
        if (not due_out) and (not out):
            raise ValidationError(
                'Either "{}" or "{}" must be set.'.format(
                    models.Lend._meta.get_field('due_out').verbose_name,
                    models.Lend._meta.get_field('out').verbose_name,
                )
            )

        # If ``back`` is set, ``out`` must also be set. That is, an item can
        # only be returned if it was earlier lent out.
        if (not out) and back:
            raise ValidationError(_a_requires_b_message(
                models.Lend._meta.get_field('back').verbose_name,
                models.Lend._meta.get_field('out').verbose_name,
            ))

        # If ``due_back`` is set, ``due_out`` must also be set. That is, an item
        # can only be due back if it was at some time due out.
        if (not due_out) and due_back:
            raise ValidationError(_a_requires_b_message(
                models.Lend._meta.get_field('due_back').verbose_name,
                models.Lend._meta.get_field('due_out').verbose_name,
            ))

        # ``due_out`` must occur before ``due_back``.
        if (due_out and due_back) and (due_out > due_back):
            raise ValidationError(_a_before_b_message(
                models.Lend._meta.get_field('due_out').verbose_name,
                models.Lend._meta.get_field('due_back').verbose_name,
            ))

        # ``out`` must occur before ``back``.
        if (out and back) and (out > back):
            raise ValidationError(_a_before_b_message(
                models.Lend._meta.get_field('out').verbose_name,
                models.Lend._meta.get_field('back').verbose_name,
            ))

# TODO: start rework

        # TODO: add explanatory message
        if due_back:
            # The existence of due_back implies the existence of due_out.
            conflicting_lends = _find_reservation_conflicts(
                item_id,
                due_out,
                due_back
            ).exclude(id__exact = self.instance.id)
            if conflicting_lends:
                # TODO: make proper error message
                raise ValidationError("error 1")
        elif due_out:
            # The existence of due_out does not imply the existence of due_back.
            conflicting_lends = _find_reservation_conflicts(item_id, due_out
            ).exclude(id__exact = self.instance.id)
            if conflicting_lends:
                # TODO: make proper error message
                raise ValidationError("error 2")

        # TODO: add explanatory message
        if back:
            # The existence of out implies the existence of back.
            conflicting_lends = _find_lend_conflicts(item_id, out, back
            ).exclude(id__exact = self.instance.id)
            if conflicting_lends:
                # TODO: make proper error message
                raise ValidationError("error 3")
        elif out:
            # The existence of `out` does not imply the existence of `back`.
            conflicting_lends = _find_lend_conflicts(item_id, out
            ).exclude(id__exact = self.instance.id)
            if conflicting_lends:
                # TODO: make proper error message
                raise ValidationError("error 4")

# TODO: end rework

        # Always return the full collection of cleaned data.
        return cleaned_data

def _a_requires_b_message(a, b):
    """Return a string stating that ``b`` must be set.

    >>> _a_requires_b_message('foo', 'bar')
    'If "foo" is set, "bar" must also be set.'

    """
    return 'If "{}" is set, "{}" must also be set.'.format(a, b)

def _a_before_b_message(a, b):
    """Return a string stating that ``a`` must occur before ``b``.

    >>> _a_before_b_message('foo', 'bar')
    '"foo" must occur before "bar".'

    """
    return '"{}" must occur before "{}".'.format(a, b)

def _already_out_message(field_name, field_value, before, after):
    """Return a string stating that ``field_name`` was already out.

    >>> _already_out_message('foo', 'bar', 'biz', 'baz')
    'Cannot set "foo" to bar. This item was out from biz to baz.'

    """
    return 'Cannot set "{}" to {}. This item was out from {} to {}.'.format(
        field_name,
        field_value,
        before,
        after
    )

def _already_reserved_message(field_name, field_value, before, after):
    """Return a string stating that ``field_name`` is already reserved.

    >>> _already_reserved_message('foo', 'bar', 'biz', 'baz')
    'Cannot set "foo" to bar. This item is reserved from biz to baz.'

    """
    return 'Cannot set "{}" to {}. This item is reserved from {} to {}.'.format(
        field_name,
        field_value,
        before,
        after
    )

def _find_reservation_conflicts(item, start, end = None):
    """Check whether ``item`` is available from ``start`` to ``end``.

    ``item`` is an ``Item`` model object. ``start`` and ``end`` are
    ``datetime.date`` objects.

    A QuerySet is returned. If ``item`` is available, the QuerySet is empty.
    Otherwise, the QuerySet contains conflicting ``Lend`` objects. One of
    several critera are used when determining whether to add a lend to the
    QuerySet.

    If ``end`` is not given:

        item == lend.item && (
            (
                # see test_conflict_v1
                Null == existing_lend.due_back
            ) || (
                # see test_conflict_v2
                Null != existing_lend.due_back &&
                start <= existing_lend.due_back
            )
        )

    If ``end`` is given:

        item == lend.item && (
            # see test_conflict_v3
            (Null == existing_lend.due_back && (
                end >= existing_lend.due_out
            )) ||
            # see test_conflict_v4
            (Null != existing_lend.due_back && (
                (
                    start >= existing_lend.due_out &&
                    start <= existing_lend.due_back
                ) || (
                    end >= existing_lend.due_out &&
                    end <= existing_lend.due_back
                ) || (
                    start <= existing_lend.due_out &&
                    end >= existing_lend.due_back
                )
            ))
        )

    """
    if None == end:
        return models.Lend.objects.filter(
            (
                # see test_conflict_v1
                Q(due_back__isnull = True) |
                # see test_conflict_v2
                (
                    Q(due_back__isnull = False) &
                    Q(due_back__gte = start)
                )
            ),
            item_id__exact = item
        )
    return models.Lend.objects.filter(
        (
            # see test_conflict_v3
            (Q(due_back__isnull = True) & (
                Q(due_out__lte = end)
            )) |
            # see test_conflict_v4
            (Q(due_back__isnull = False) & (
                (
                    Q(due_out__lte = start) &
                    Q(due_back__gte = start)
                ) | (
                    Q(due_out__lte = end) &
                    Q(due_back__gte = end)
                ) | (
                    Q(due_out__gte = start) &
                    Q(due_back__lte = end)
                )
            ))
        ),
        item_id__exact = item
    )

def _find_lend_conflicts(item, start, end = None):
    """Check whether ``item`` is available from ``start`` to ``end``.

    ``item`` is an ``Item`` model object. ``start`` and ``end`` are
    ``datetime.datetime`` objects.

    A QuerySet is returned. If ``item`` can be lent out, the QuerySet is empty.
    Otherwise, the QuerySet contains conflicting ``Lend`` objects. To be more
    exact, the following criteria is used when searching for lends to add to the
    QuerySet:

        item == lend.item && (
            (
                start <= lend.out &&
                end   >= lend.out
            ) || (
                Null  != lend.back &&
                start >= lend.back
            )
        )

    If ``end`` is not specified, it defaults to infinity.

    """
    if None == end:
        return models.Lend.objects.filter(
            (
                # see test_conflict_v5
                Q(back__isnull = True) |
                # see test_conflict_v6
                (
                    Q(back__isnull = False) &
                    Q(back__gte = start)
                )
            ),
            item_id__exact = item
        )
    return models.Lend.objects.filter(
        (
            # see test_conflict_v7
            (Q(back__isnull = True) & (
                Q(out__lte = end)
            )) |
            # see test_conflict_v8
            (Q(back__isnull = False) & (
                (
                    Q(out__lte = start) &
                    Q(back__gte = start)
                ) | (
                    Q(out__lte = end) &
                    Q(back__gte = end)
                ) | (
                    Q(out__gte = start) &
                    Q(back__lte = end)
                )
            ))
        ),
        item_id__exact = item
    )

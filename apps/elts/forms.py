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

class CategoryForm(ModelForm):
    """A form for a Catgory."""

    class Meta(object):
        """Form attributes that are not fields.

        Note that, although ``user`` is a required attribute of the ``Category``
        model, it is not included in this form. The user should never have a
        chance to set that particular form field, so including it here does not
        make sense. Instead, it is the responsibility of views to set that
        attribute.

        So how is that done? One cannot simply set 'user' on this form while or
        after creating it.

        >>> from django.db import IntegrityError
        >>> category_form = CategoryForm({'name': 'test', 'user': 1})
        >>> try:
        ...     category_form.save()
        ... except IntegrityError:
        ...     pass

        Instead, one must create a ``Category`` object from the form, muck with
        that object, save the object and save its many-to-many relationships.

        >>> from elts import factories
        >>> category_form = CategoryForm({'name': 'test'})
        >>> category = category_form.save(commit = False)
        >>> category.user = factories.UserFactory.create()
        >>> category.save()
        >>> category_form.save_m2m()

        For more information, see
        https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method

        """
        model = models.Category
        fields = ['name', 'tags']

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
    def clean(self):
        """Perform form-wide validation.

        This method is called after ``Field.clean()`` has been called on each
        individual field. "Any ValidationError raised by this method will
        not be associated with a particular field; it will have a special-case
        association with the field named '__all__'."

        """
        # Let the parent class do some checks.
        cleaned_data = super(LendForm, self).clean()
        # Grab data necessary for validation.
        item_id = cleaned_data.get('item_id')
        due_out = cleaned_data.get('due_out')
        due_back = cleaned_data.get('due_back')
        out = cleaned_data.get('out')
        back = cleaned_data.get('back')
        # The conflict detection code uses this.
        conflicting_lends = []

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

        # Check whether ``due_out`` and/or ``due_back`` conflict with existing
        # reservations.
        conflicting_lends = _find_reservation_conflicts(
            item_id,
            due_out,
            due_back
        ).exclude(id__exact = self.instance.id)
        if conflicting_lends:
            raise ValidationError(_already_reserved_message(
                due_out,
                due_back,
                conflicting_lends
            ))

        # Check whether ``out`` and/or ``back`` conflict with existing lends.
        conflicting_lends = _find_lend_conflicts(
            item_id,
            out,
            back
        ).exclude(id__exact = self.instance.id)
        if conflicting_lends:
            raise ValidationError(_already_out_message(
                out,
                back,
                conflicting_lends
            ))

        # Always return the full collection of cleaned data.
        return cleaned_data

def _infinity_if_none(obj):
    """Return 'infinity' if ``obj`` is None, else ``obj``.

    >>> _infinity_if_none('foo')
    'foo'
    >>> _infinity_if_none(None)
    'infinity'

    """
    if obj is None:
        return 'infinity'
    return obj

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

def _already_out_message(start, end, conflicting_lends):
    """Return a string stating that an item is lent out from ``start`` to
    ``end``.

    ``start`` is a ``datetime.datetime`` object.

    ``end`` is either a ``datetime.datetime`` object or ``None``.

    ``conflicting_lends`` is an iterable of ``Lend`` model objects.

    >>> from elts import factories
    >>> from datetime import timedelta
    >>> message = _already_out_message(
    ...     factories.lend_out(),
    ...     None,
    ...     []
    ... )
    >>> isinstance(message, str)
    True
    >>> message = _already_out_message(
    ...     factories.lend_out(),
    ...     None,
    ...     [factories.PastLendFactory.build()]
    ... )
    >>> isinstance(message, str)
    True
    >>> message = _already_out_message(
    ...     factories.lend_out(),
    ...     factories.lend_back(),
    ...     [
    ...         factories.PastLendFactory.build(),
    ...         factories.PastLendFactory.build()
    ...     ]
    ... )
    >>> isinstance(message, str)
    True

    """
    message = 'Cannot lend item from {} to {}.'.format(
        start,
        _infinity_if_none(end)
    )
    if 1 < len(conflicting_lends):
        message += 'There are {} conflicting lends: '.format(len(conflicting_lends))
    elif 1 == len(conflicting_lends):
        message += 'There is 1 conflicting lend: '
    else:
        message += "I don't know why. Something has gone horribly wrong.."

    # list conflicting dates
    message += ', '.join([
        'from {} to {}'.format(conflict.out, _infinity_if_none(conflict.back))
        for conflict
        in conflicting_lends
    ]) + '.'

    return message

def _already_reserved_message(start, end, conflicting_lends):
    """Return a string stating that an item is reserved from ``start`` to
    ``end``.

    ``start`` is a ``datetime.date`` object.

    ``end`` is either a ``datetime.date`` object or ``None``.

    ``conflicting_lends`` is an iterable of ``Lend`` model objects.

    >>> from elts import factories
    >>> from datetime import timedelta
    >>> message = _already_out_message(
    ...     factories.lend_due_out(),
    ...     None,
    ...     []
    ... )
    >>> isinstance(message, str)
    True
    >>> message = _already_out_message(
    ...     factories.lend_due_out(),
    ...     None,
    ...     [factories.FutureLendFactory.build()]
    ... )
    >>> isinstance(message, str)
    True
    >>> message = _already_out_message(
    ...     factories.lend_due_out(),
    ...     factories.lend_due_back(),
    ...     [
    ...         factories.FutureLendFactory.build(),
    ...         factories.FutureLendFactory.build()
    ...     ]
    ... )
    >>> isinstance(message, str)
    True

    """
    message = 'Cannot reserve item from {} to {}. '.format(
        start,
        _infinity_if_none(end)
    )
    if 1 < len(conflicting_lends):
        message += 'There are {} conflicting reservations: '.format(len(conflicting_lends))
    elif 1 == len(conflicting_lends):
        message += 'There is 1 conflicting reservation: '
    else:
        message += "I don't know why. Something has gone horribly wrong.."

    # list conflicting dates
    message += ', '.join([
        'from {} to {}'.format(
            conflict.due_out,
            _infinity_if_none(conflict.due_back)
        )
        for conflict
        in conflicting_lends
    ]) + '.'

    return message

def _find_reservation_conflicts(item, start = None, end = None):
    """Check whether ``item`` is available from ``start`` to ``end``.

    ``item`` is an ``Item`` model object. ``start`` and ``end`` are
    ``datetime.date`` objects.

    A QuerySet is returned. If ``item`` can be reserved, the QuerySet is empty.
    Otherwise, the QuerySet contains conflicting ``Lend`` objects. One of
    several critera are used when determining whether to add a lend to the
    QuerySet.

    If ``start`` is not given, an empty QuerySet is immediately returned.

    If ``start`` is given:

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

    If ``start`` and ``end`` are given:

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
    if start is None:
        return models.Lend.objects.none()

    if (start is not None) and (end is None):
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

    # start and end should be present
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

def _find_lend_conflicts(item, start = None, end = None):
    """Check whether ``item`` is available from ``start`` to ``end``.

    ``item`` is an ``Item`` model object. ``start`` and ``end`` are
    ``datetime.datetime`` objects.

    A QuerySet is returned. If ``item`` can be lent out, the QuerySet is empty.
    Otherwise, the QuerySet contains conflicting ``Lend`` objects. To be more
    several critera are used when determining whether to add a lend to the
    QuerySet.

    If ``start`` is not given, an empty QuerySet is immediately returned.

    If ``start`` is given:

        item == lend.item && (
            (
                # see test_conflict_v5
                Null == existing_lend.back
            ) || (
                # see test_conflict_v6
                Null != existing_lend.back &&
                start <= existing_lend.back
            )
        )

    If ``start`` and ``end`` are given:

        item == lend.item && (
            # see test_conflict_v7
            (Null == existing_lend.back && (
                end >= existing_lend.out
            )) ||
            # see test_conflict_v8
            (Null != existing_lend.back && (
                (
                    start >= existing_lend.out &&
                    start <= existing_lend.back
                ) || (
                    end >= existing_lend.out &&
                    end <= existing_lend.back
                ) || (
                    start <= existing_lend.out &&
                    end >= existing_lend.back
                )
            ))
        )

    """
    if start is None:
        return models.Lend.objects.none()

    if (start is not None) and (end is None):
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

    # start and end should be present
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

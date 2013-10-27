"""Forms for creating and updating objects.

Unless otherwise noted, all forms defined herein can be used to either create or
update an object.

"""
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
        """Model attributes that are not fields."""
        model = models.Item
        fields = ['name', 'description', 'tags', 'is_lendable']
        widgets = {'description': widgets.Textarea()}

class TagForm(ModelForm):
    """A form for a Tag."""

    class Meta(object):
        """Model attributes that are not fields."""
        model = models.Tag
        fields = ['name', 'description']
        widgets = {'description': widgets.Textarea()}

# Start `NoteForm` definitions.

class ItemNoteForm(ModelForm):
    """A form for a ItemNote."""

    class Meta(object):
        """Model attributes that are not fields."""
        model = models.ItemNote
        fields = ['note_text']
        widgets = {'note_text': widgets.Textarea()}

class UserNoteForm(ModelForm):
    """A form for a UserNote."""

    class Meta(object):
        """Model attributes that are not fields."""
        model = models.UserNote
        fields = ['note_text']
        widgets = {'note_text': widgets.Textarea()}

class LendNoteForm(ModelForm):
    """A form for a LendNote."""

    class Meta(object):
        """Model attributes that are not fields."""
        model = models.LendNote
        fields = ['is_complaint', 'note_text']
        widgets = {'note_text': widgets.Textarea()}

# End `NoteForm` definitions.

class LoginForm(Form):
    """A form for logging in a ``User``."""
    username = CharField()
    password = CharField(widget = widgets.PasswordInput)

    class Meta(object):
        """Model attributes that are not fields."""
        fields = ['username', 'password']

class LendForm(ModelForm):
    """A form for a Lend."""

    class Meta(object):
        """Model attributes that are not fields."""
        model = models.Lend
        fields = ['item_id', 'user_id', 'due_out', 'due_back', 'out', 'back']
        widgets = {
            'due_out':  widgets.DateInput(attrs = {'type': 'date'}),
            'due_back': widgets.DateInput(attrs = {'type': 'date'}),
            'out':  widgets.DateTimeInput(attrs = {'type': 'datetime'}),
            'back': widgets.DateTimeInput(attrs = {'type': 'datetime'}),
        }

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
        due_out = cleaned_data.get('due_out')
        due_back = cleaned_data.get('due_back')
        out = cleaned_data.get('out')
        back = cleaned_data.get('back')

        # FIXME: push each check into a private helper function. Write doctests
        # for each of those functions.
        # FIXME: add a check to ensure that a given item isn't being lent out
        # twice

        # Either ``due_out`` or ``out`` must be set; ``Lend`` objects keep track
        # of item reservations and lends.
        if (not due_out) and (not out):
            raise ValidationError(
                'Either "{}" or "{}" must be set.'.format(
                    models.Lend._meta.get_field('due_out').verbose_name,
                    models.Lend._meta.get_field('out').verbose_name,
                )
            )

        # An item can only be returned if it was earlier lent out.
        if (not out) and back:
            raise ValidationError(
                'If "{}" is set, "{}" must also be set.'.format(
                    models.Lend._meta.get_field('back').verbose_name,
                    models.Lend._meta.get_field('out').verbose_name,
                )
            )

        # If an item is due out and due back, the former must take place before
        # the latter.
        if (due_out and due_back) and (due_out > due_back):
            raise ValidationError(
                '"{}" must occur before "{}".'.format(
                    models.Lend._meta.get_field('due_out').verbose_name,
                    models.Lend._meta.get_field('due_back').verbose_name,
                )
            )

        # If an item has been lent out and returned, the former must have taken
        # place before the latter.
        if (out and back) and (out > back):
            raise ValidationError(
                '"{}" must occur before "{}".'.format(
                    models.Lend._meta.get_field('out').verbose_name,
                    models.Lend._meta.get_field('back').verbose_name,
                )
            )

        # Always return the full collection of cleaned data.
        return cleaned_data

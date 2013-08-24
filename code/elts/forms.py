"""Forms for creating and updating objects.

Unless otherwise noted, all forms defined herein can be used to either create or
update an object.

"""
from django.contrib.auth.models import User
from django.forms.forms import NON_FIELD_ERRORS
from django.forms import CharField, Form, ModelForm
from django.forms.util import ErrorList
from django.forms.widgets import PasswordInput, Textarea
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
    class Meta:
        model = models.Item
        fields = ['name', 'description', 'tags', 'is_lendable']
        widgets = {'description': Textarea()}

class TagForm(ModelForm):
    """A form for a Tag."""
    class Meta:
        model = models.Tag
        fields = ['name', 'description']
        widgets = {'description': Textarea()}

# Start `NoteForm` definitions.

class ItemNoteForm(ModelForm):
    """A form for a ItemNote."""
    class Meta:
        model = models.ItemNote
        fields = ['note_text']
        widgets = {'note_text': Textarea()}

class UserNoteForm(ModelForm):
    """A form for a UserNote."""
    class Meta:
        model = models.UserNote
        fields = ['note_text']

class LendNoteForm(ModelForm):
    """A form for a LendNote."""
    class Meta:
        model = models.LendNote
        fields = ['is_complaint', 'note_text']

# End `NoteForm` definitions.

class LoginForm(Form):
    """A form for logging in a ``User``."""
    username = CharField()
    password = CharField(widget = PasswordInput)

    class Meta:
        fields = ['username', 'password']

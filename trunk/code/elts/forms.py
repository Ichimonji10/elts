"""Forms for creating and updating objects.

Unless otherwise noted, all forms defined herein can be used to either create or
update an object.

"""
from django import forms
from elts import models

# pylint: disable=R0903
# "Too few public methods (0/2)" 
# It is both common and OK for a model to have no methods.
#
# pylint: disable=W0232
# "Class has no __init__ method" 
# It is both common and OK for a model to have no __init__ method.

class ItemForm(forms.ModelForm):
    """A form for an Item."""
    class Meta:
        model = models.Item
        fields = ['name', 'description', 'tags']

class TagForm(forms.ModelForm):
    """A form for a Tag."""
    class Meta:
        model = models.Tag
        fields = ['name', 'description']

# Start `NoteForm` definitions.

class ItemNoteForm(forms.ModelForm):
    """A form for a ItemNote."""
    class Meta:
        model = models.ItemNote
        fields = ['note_text']

class PersonNoteForm(forms.ModelForm):
    """A form for a PersonNote."""
    class Meta:
        model = models.PersonNote
        fields = ['note_text']

class ReservationNoteForm(forms.ModelForm):
    """A form for a ReservationNote."""
    class Meta:
        model = models.ReservationNote
        fields = ['note_text']

class LendNoteForm(forms.ModelForm):
    """A form for a LendNote."""
    class Meta:
        model = models.LendNote
        fields = ['note_text']

# End `NoteForm` definitions.

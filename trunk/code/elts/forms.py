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
    """A form for creating an Item."""
    class Meta:
        model = models.Item
        fields = ['name', 'description', 'tags']

class TagForm(forms.ModelForm):
    """A form for creating a Tag."""
    class Meta:
        model = models.Tag
        fields = ['name', 'description']

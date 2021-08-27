from django import forms
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Item


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'starting_price',
                  'image_url', 'categories')
        labels = {
            'name': _('Item name'),
            'image_url': _('Image URL')
        }
        form_control = {'class': 'form-control'}  # Bootstrap class
        widgets = {
            'name': forms.TextInput(attrs=form_control),
            'description': forms.Textarea(attrs=form_control),
            'starting_price': forms.NumberInput(attrs=form_control),
            'image_url': forms.URLInput(attrs=form_control),
            'categories': forms.CheckboxSelectMultiple
        }

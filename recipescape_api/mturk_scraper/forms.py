from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ScrapedRecipe


class ScrapedForm(forms.ModelForm):
    class Meta:
        model = ScrapedRecipe
        fields = ['title', 'image_url', 'ingredients', 'instruction']
        labels = {
            'title': _('Title of Recipe'),
            'image_url': _('URL of Image (optional)'),
        }

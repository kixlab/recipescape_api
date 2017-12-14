from django import forms
from .models import ScrapedRecipe


class ScrapedForm(forms.ModelForm):
    class Meta:
        model = ScrapedRecipe
        fields = ['title', 'image_url', 'ingredients', 'instruction']


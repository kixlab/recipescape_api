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
            'ingredients': _('Ingredients (please put one ingredient in one line'),
        }
        widgets = {
            'ingredients': forms.Textarea(attrs={
                'placeholder': '1 lb pork tenderloin, trimmed of silver skin and excess fat\n1/4 cup soy sauce\n3 cloves garlic, minced'
            }),
            'instruction': forms.Textarea(attrs={
                'placeholder': 'Place the pork in the freezer until it firms up, about 1 hour. While the pork is in the freezer, combine the soy sauce, garlic, brown sugar, gochujang , mirin, sesame oil, ginger, red pepper flakes, and green onions in a small bowl.\n\nRemove the pork from the freezer and slice into pieces 1/8 inch thick. Place the pork and sliced onion in a large Ziploc bag, pour in the marinade and seal. Toss to evenly distribute the marinade, then open and reseal the bag, removing as much air as possible. Place in the refrigerator and let marinate for at least one hour to overnight.\n\nLight one chimney full of charcoal. When all the charcoal is lit and covered with gray ash, pour out and spread the coals evenly over the charcoal grate. Clean and oil the grilling grate. Place the pork slices on the grill and cook until the meat is seared on both sides and cooked through, about 1 minute per side. Remove from the grill and serve immediately with bibb lettuce, kimchi, and quick pickles.'
            })
        }

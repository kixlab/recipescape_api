# Register your models here.
from django.contrib import admin
from .models import Recipe, Annotation

class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('title', )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Annotation)

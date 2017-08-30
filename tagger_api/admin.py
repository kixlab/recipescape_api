# Register your models here.
from django.contrib import admin
from .models import Recipe, Annotation


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_filter = ('group_name', )
    list_display = ('origin_id', 'title', 'last_assigned', 'is_unused', )
    list_editable = ('is_unused', )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Annotation)

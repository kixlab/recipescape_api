from django.contrib import admin
# Register your models here.
from .models import RecipeURL, Assignment, ScrapedRecipe


class URLAdmin(admin.ModelAdmin):
    list_display = ('url', 'group_name')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('url', 'started_at', 'finished_at', 'token')


admin.site.register(RecipeURL, URLAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(ScrapedRecipe)


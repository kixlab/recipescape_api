# Register your models here.
from django.contrib import admin
from django.db.models import Count
from .models import Recipe, Annotation


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('title', 'origin_id', )
    list_filter = ('group_name', )
    list_display = ('origin_id', 'title', 'last_assigned', 'is_unused', )
    list_editable = ('is_unused', )


class AnnotationAdmin(admin.ModelAdmin):
    search_fields = ('recipe__origin_id', )
    list_display = ('annotator', 'worker', 'annotated_at', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Annotation, AnnotationAdmin)

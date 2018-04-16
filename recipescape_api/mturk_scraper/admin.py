from django.contrib import admin
from django.db.models import Count
# Register your models here.
from .models import RecipeURL, Assignment, ScrapedRecipe


class ScrapedRecipeAdmin(admin.ModelAdmin):
    list_display = ('title', )


class URLAdmin(admin.ModelAdmin):
    list_display = ('url', 'group_name', 'num_finished')

    def get_queryset(self, request):
        return RecipeURL.objects.annotate(
            num_finished=Count('assignment__finished_at'))

    def num_finished(self, obj):
        return obj.num_finished

    num_finished.admin_order_field = 'num_finished'


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('url', 'started_at', 'finished_at', 'token')


admin.site.register(RecipeURL, URLAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(ScrapedRecipe, ScrapedRecipeAdmin)


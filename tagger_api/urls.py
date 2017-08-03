from django.conf.urls import url

from tagger_api import views, views_rest

urlpatterns = [
    url(r'^recipe$', views_rest.new_recipe),
    url(r'^recipe/(\S+)', views_rest.get_recipe),
    url(r'^annotate/(\S+)', views_rest.Annotation.as_view())
    # url(r'^(\S+)/save$', views.save_annotation, name='save_annotation'),
    # url(r'^(\S+)$', views.get_recipe, name='get_recipe'),
]

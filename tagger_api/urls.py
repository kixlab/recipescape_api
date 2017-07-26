from django.conf.urls import url

from tagger_api import views

urlpatterns = [
    url(r'^new$', views.new_recipe, name='new_recipe'),
    url(r'^(\S+)/save$', views.save_annotation, name='save_annotation'),
    url(r'^(\S+)$', views.get_recipe, name='get_recipe'),
]

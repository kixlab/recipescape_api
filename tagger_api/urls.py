from django.conf.urls import url

from tagger_api import views

urlpatterns = [
    url(r'^recipe$', views.new_recipe),
    url(r'^recipe/(\S+)', views.get_recipe),
    url(r'^annotation/(\S+)', views.AnnotationView.as_view())
]

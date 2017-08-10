from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^recipe/(\S+)', views.get_recipe),
]

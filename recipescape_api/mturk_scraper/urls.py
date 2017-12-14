from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^contribute$', views.start_work),
]

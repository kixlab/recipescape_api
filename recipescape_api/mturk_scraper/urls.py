from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^start$', views.route_work),
    url(r'^contribute$', views.start_work, name='start_work'),
    url(r'^contribute/result$', views.show_result, name='show_result'),
]

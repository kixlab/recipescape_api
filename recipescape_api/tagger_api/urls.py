from django.conf.urls import url

from tagger_api import views

urlpatterns = [
    url(r'^recipe$', views.new_recipe),
    url(r'^recipe/(\S+)', views.get_recipe),
    url(r'^annotation/(\S+)', views.AnnotationView.as_view()),
    url(r'^user$', views.get_userinfo),
    url(r'^status$', views.leaderboard),
    url(r'^status/(\S+)', views.count_corrections),
]

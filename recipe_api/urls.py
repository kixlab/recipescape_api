from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^recipe/(?P<recipe_id>\w+)', views.get_recipe),
    url(r'^recipes/(?P<dish>\w+)', views.get_recipes),
    url(r'^clusters/(?P<dish>\w+)', views.get_clusters),
    url(r'^tree/(?P<recipe_id>\w+)', views.get_tree),
    url(r'^trees/(?P<dish>\w+)', views.get_trees),
    url(r'^nodes', views.get_nodes_by_ids),
    url(r'^nodes/(?P<dish>\w+)', views.get_nodes),
    url(r'^histogram/(?P<dish>\w+)', views.get_action_ingredient_histogram),
    url(r'^histograms/(?P<dish>\w+)', views.get_histograms),
]

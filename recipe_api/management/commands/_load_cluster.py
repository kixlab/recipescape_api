import numpy as np

from recipe_api.models import Clustering


def load_cluster(title, dish_name, points_path, centers_path):
    recipes = np.load(points_path)
    recipes = recipes.A # they are matrix
    points = []
    for recipe in recipes:
        points.append({
            'x': float(recipe[1]),
            'y': float(recipe[2]),
            'cluster_no': int(recipe[3]),
            'recipe_id': recipe[0],
        })

    centers_np = np.load(centers_path)
    centers = {}
    for center in centers_np:
        cluster_no = int(center[0][3])
        center_id = center[0][0]
        centers[cluster_no] = center_id

    cluster_result = Clustering.objects.create(title=title,
                                               dish_name=dish_name,
                                               points=points,
                                               centers=centers)
    cluster_result.save()

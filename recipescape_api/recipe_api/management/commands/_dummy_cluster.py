import random

import numpy as np
from sklearn.cluster import KMeans

from recipe_api.models import Clustering
from tagger_api.models import Recipe


def run_cluster(title, dish_name):
    dishes = Recipe.objects.filter(group_name=dish_name).values_list('origin_id')
    xy = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in dishes])
    kmeans = KMeans(n_clusters=10, n_jobs=-2, verbose=1).fit(xy)

    points = []
    for i, dish in enumerate(dishes):
        point = {
            'x': float(xy[i][0]),
            'y': float(xy[i][1]),
            'cluster_no': int(kmeans.labels_[i]),
            'recipe_id': dishes[i][0],
        }
        points.append(point)

    print(kmeans.cluster_centers_)

    centers = {}
    for i, center in enumerate(kmeans.cluster_centers_):
        distances = [(p['recipe_id'], ((p['x'] - center[0])**2 + (p['y'] - center[1])**2))
                     for p in points
                     if p['cluster_no'] == i]
        median = min(distances, key=lambda p: p[1])
        centers[i] = median[0]

    cluster_result = Clustering.objects.create(title=title,
                                               dish_name=dish_name,
                                               points=points,
                                               centers=centers)
    cluster_result.save()

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def plot(data, centroids=None, n=None, filename=None, truth=None):
    if truth: key = 'truth'
    else: key = 'cluster'
    cluster = map(lambda d: d[key], data)
    points = map(lambda d: d['expressions'], data)

    fig, ax = plt.subplots()
    if centroids:
        colors = iter(cm.rainbow(np.linspace(0, 1, len(centroids))))
        c_centroids = map(lambda d: d['expressions'], centroids)
        c_cluster = range(1,len(centroids)+1)
        points.extend(c_centroids)
        cluster.extend(c_cluster)
        n = len(centroids)
    elif n:
        colors = iter(cm.rainbow(np.linspace(0, 1, n)))
    pca = PCA(n_components=2)
    pca.fit(points)
    fitted = pca.transform(points)
    for i in range(n):
        c = next(colors)
        ids = [q for q, x in enumerate(cluster) if x == i+1]
        c_points = fitted[ids, :]
        if centroids:
            centroid = c_points[(-1), :]
            plt.scatter(centroid[0], centroid[1], color=c, marker='x', s=80)

        if len(c_points):
            if c_points.shape[1] == 2:
                plt.scatter(c_points[:, 0], c_points[:, 1], color=c)
        # break
    plt.show()
    if filename:
        fig.savefig(filename)
        plt.close(fig)
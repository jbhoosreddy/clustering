from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def plot(data, centroids=None, n=None, filename=None, truth=None):

    fig, ax = plt.subplots()
    if centroids:
        colors = iter(cm.rainbow(np.linspace(0, 1, len(centroids))))
        centroids = map(lambda d: d['expressions'], centroids)
        pca = PCA(n_components=2)
        fitted_centroids = pca.fit_transform(centroids)
        n = len(centroids)
    elif n:
        colors = iter(cm.rainbow(np.linspace(0, 1, n)))
    for i in range(n):
        pca = PCA(n_components=2)
        c = next(colors)
        if centroids:
            centroid = fitted_centroids[i]
            plt.scatter(centroid[0], centroid[1], color=c, marker='x', s=80)
        if truth:
            points = map(lambda f: f['expressions'], filter(lambda d: d['truth'] == i + 1, data))
        else:
            points = map(lambda f: f['expressions'], filter(lambda d: d['cluster'] == i + 1, data))
        if len(points):
            fitted = pca.fit_transform(points)
            if fitted.shape[1] == 2:
                plt.scatter(fitted[:, 0], fitted[:, 1], color=c)
        # break
    plt.show()
    if filename:
        fig.savefig(filename)
        plt.close(fig)
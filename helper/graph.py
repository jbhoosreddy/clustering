from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def plot(data, centroids):
    points = map(lambda d: d['expressions'], data)
    pca = PCA(n_components=2)
    fitted = pca.fit_transform(points)
    l = len(fitted)
    fig, ax = plt.subplots()
    plt.scatter(fitted[:, 0], fitted[:, 1])
    plt.show()
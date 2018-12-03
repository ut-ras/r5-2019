from vision.k_means.kernel_kmeans import kernel_kmeans
import mnist
import numpy as np

images = mnist.train_images()[:1000]
labels = mnist.train_labels()[:1000]

images = np.array([img for i, img in enumerate(images) if labels[i] in [1, 2]])
labels = [val for i, val in enumerate(labels) if val in [1, 2]]


def get_label(x):
    for i, xa in enumerate(images):
        if np.array_equal(x, xa):
            return labels[i]

    return "NOLABEL"


c = kernel_kmeans(images, None, 2, 0.05)
ind = 0

for ind, cluster in enumerate(c):
    print("BEGIN CLUSTER", ind)

    for x in cluster:
        print(get_label(x), end="")

    print()

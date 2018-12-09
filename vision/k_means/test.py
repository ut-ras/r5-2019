from vision.k_means.kernel_kmeans import kernel_kmeans, k_gauss
import mnist
import numpy as np
import sys

images = mnist.train_images()[:1000]
images = images.reshape((images.shape[0], images.shape[1] * images.shape[2]))
labels = mnist.train_labels()[:1000]

data, idents = [], []
clusters = [1, 2, 3, 4]
sample_size = 250

for ind, img in enumerate(images):
    if len(data) == sample_size:
        break

    if labels[ind] in clusters:
        data.append(img)
        idents.append(ind)


images = np.array([img for i, img in enumerate(images) if labels[i] in [1, 2]])
labels = [val for val in labels if val in [1, 2]]


def get_label(x):
    for i, xa in enumerate(data):
        if np.array_equal(x, xa):
            return idents[i]

    return "NOLABEL"


#a, b, c = images[0], images[1], images[2]
#f1, f2 = k_gauss(a, b, 0), k_gauss(a, c, 0)
#print(get_label(a), "and", get_label(b), "produced", f1)
#print(get_label(a), "and", get_label(c), "produced", f2)
#sys.exit(0)

print("Loaded " + str(len(data)) + " points")


c = kernel_kmeans(data, len(clusters), 0.05)
ind = 0

for ind, cluster in enumerate(c):
    print("BEGIN CLUSTER", ind)

    for x in cluster:
        print(get_label(x), end="")

    print()

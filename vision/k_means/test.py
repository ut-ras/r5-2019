from .kernel_kmeans import kernel_kmeans
import numpy as np

n = 10
m = 10
x = np.array([np.array([np.random.uniform(0, 5) for a in range(m)]) for b in range(n)])
c = kernel_kmeans(x, None, 3, 0.05)
print(c)
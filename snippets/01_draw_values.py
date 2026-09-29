"""Draw values from one normal distribution."""

import numpy as np

mean = 0
std_dev = 1
size = 1000
seed = 404
rng = np.random.default_rng(seed)

values = rng.normal(loc=mean, scale=std_dev, size=size)

print("Number of values:", len(values))
print("First five values:", values[:5])

import numpy as np
import matplotlib.pyplot as plt



r = 0
for angle in np.arange(0, 360, 2):
    r += 0.4
    x = r*np.cos(angle)
    y = r*np.sin(angle)

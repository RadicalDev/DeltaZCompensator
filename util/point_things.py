__author__ = 'jfindley'
import matplotlib.pyplot as plt
import math


xa = range(-50, 50)
ya = range(-50, 50)
last_x = 0
last_y = 0
for x in xa:
    for y in ya:
        if x**2 + y**2 > 50:
            continue
        v = (x-last_x, y-last_y)
        print math.atan2(*v)*(180/math.pi)
        last_x = x
        last_y = y
        plt.scatter(x, y)
        plt.scatter(*v, color='red')
plt.show()

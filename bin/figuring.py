__author__ = 'jfindley'


t = """X: 40, Y: 40, Z: -0.04, M: -0.0
X: 40, Y: 20, Z: 0.06, M: -0.0
X: 40, Y: 0, Z: 0.12, M: -0.01
X: 40, Y: -20, Z: 0.14, M: -0.02
X: 40, Y: -40, Z: 0.12, M: -0.0
X: 20, Y: 40, Z: 0.03, M: -0.01
X: 20, Y: 20, Z: 0.08, M: -0.01
X: 20, Y: 0, Z: 0.11, M: -0.01
X: 20, Y: -20, Z: 0.13, M: -0.01
X: 20, Y: -40, Z: 0.11, M: -0.01
X: 0, Y: 60, Z: 0.01, M: -0.01
X: 0, Y: 40, Z: 0.02, M: -0.01
X: 0, Y: 20, Z: 0.05, M: -0.02
X: 0, Y: 0, Z: 0.07, M: -0.02
X: 0, Y: -20, Z: 0.12, M: -0.01
X: 0, Y: -40, Z: 0.12, M: -0.01
X: -20, Y: 40, Z: 0.03, M: -0.02
X: -20, Y: 20, Z: 0.01, M: -0.02
X: -20, Y: 0, Z: 0.07, M: -0.01
X: -20, Y: -20, Z: 0.11, M: -0.01
X: -20, Y: -40, Z: 0.11, M: -0.02
X: -40, Y: 40, Z: -0.05, M: 0.04
X: -40, Y: 20, Z: -0.04, M: 0.02
X: -40, Y: 0, Z: 0.04, M: -0.02
X: -40, Y: -20, Z: 0.09, M: -0.02
X: -40, Y: -40, Z: 0.1, M: -0.03
X: -60, Y: 0, Z: -0.14, M: 0.13""".splitlines()

import re


def actual_z(z, m):
    return -z+m

def new_z(z, m):
    return z + -m

def shouldbezero(az, zn):
    return az + zn

for i in t:
    x, y, z, m = [float(x) for x in re.findall("(-?\d+(?:\.\d+)?)", i)]
    az = actual_z(z, m)
    zn = new_z(z, m)
    print az, zn, shouldbezero(az, zn)


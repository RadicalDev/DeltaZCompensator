__author__ = 'jfindley'
import os
import numpy as np


class KDTreeInterpolationEngine(object):
    def __init__(self, map, k=3, w=0.001):
        self.zmap = []
        self.XY = None
        self.Z = None
        self.tree = None
        self.map = map

        if not os.path.exists(map):
            raise Exception("File not found: {0}".format(map))

        self.load_zmap()
        self.generate_kdtree(*self.zmap)

    def load_zmap(self):
        with open(self.map, 'r') as f:
            zmap_data = f.readlines()

        X = []
        Y = []
        Z = []

        for line in zmap_data:
            x, y, z = line.split(",")
            X.append(float(x.strip()))
            Y.append(float(y.strip()))
            Z.append(float(z.strip()))
        self.zmap = (X, Y, Z)

    def generate_kdtree(self, X, Y, Z):
        from scipy.spatial import cKDTree
        self.XY = np.array(zip(X, Y))
        self.Z = np.array(Z)
        self.tree = cKDTree(self.XY)

    def get_z_offset(self, x, y, layer_height=0):
        xy = np.array([x,y])
        distances, indices = self.tree.query(xy, k=2)
        z_vals = self.Z[indices]
        delta_z = np.average(z_vals, weights=[(0.001/j) if j else 1 for j in distances])
        if not delta_z:
            delta_z = 0.00
        return layer_height + (-delta_z)
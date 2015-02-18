__author__ = 'jfindley'
import sys
import os
sys.path.append(os.path.join("..", "lib"))
import time
import numpy as np
from printer import OrionDelta
from dial_indicator import HF93295


class Map(object):
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.zmap = []
        self.XY = None
        self.Z = None

    def load_zmap(self):
            with open(self.csv_file, 'r') as f:
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
            print "Loaded ZMAP"

    def generate_kdtree(self, X, Y, Z):
        from scipy.spatial import cKDTree
        self.XY = np.array(zip(X, Y))
        self.Z = np.array(Z)
        self.tree = cKDTree(self.XY)

    def get_z_offset_literal(self, x, y):
        XYZ = zip(*self.zmap)
        for triplet in XYZ:
            if triplet[0] == x and triplet[1] == y:
                return triplet[2]
        return 0.00

    def get_z_offset_kdtree(self, x, y, k=2):
        xy = np.array([x,y])
        distances, indices = self.tree.query(xy, k=k)
        if isinstance(distances, float):
            weights = 1
        else:
            weights = np.array([(2/j) if j else 1 for j in distances])

        print "Distances: ", distances
        print "Indices: ", indices
        z_vals = self.Z[indices]

        print "z_vals: ", z_vals
        delta_z = np.average(z_vals, weights=[(0.001/j) if j else 1 for j in distances])

        if not delta_z:
            delta_z = 0.00
        return delta_z


if __name__ == "__main__":
    map = Map("../csv/zmap_10mm_r75_updown.csv")
    map.load_zmap()
    map.generate_kdtree(*map.zmap)
    printer = OrionDelta("/dev/ttyACM0", 115200)
    printer.connect()

    dial = HF93295("/dev/ttyACM1", 115200)
    k = 1
    w = 0.001
    x, y = 0, 0
    z = 0
    use_tree = False
    while True:
        command = raw_input("Enter: ")

        try:
            if command.startswith("k"):
                k = int(command[1:])
            elif command.startswith("w"):
                w = float(command[1:])
            elif command.startswith('z'):
                z = float(command[1:])
            elif command.startswith("u"):
                use_tree = not use_tree
            else:
                try:
                    x, y, z = [float(c) for c in command.split(",")]
                    if use_tree:
                        z = z + map.get_z_offset_kdtree(x, y, k=k)
                except:
                    x, y = [float(c) for c in command.split(",")]
                    z = map.get_z_offset_kdtree(x, y, k=k)
        except:
            continue

        printer.write("G1 S1 X{0} Y{1} Z{2}".format(x, y, z))
        time.sleep(1)
        measurement = dial.read()
        print "{0}, {1} [{2}] -> {3} (k={4}, w={5})".format(x, y, z, measurement, k, w)

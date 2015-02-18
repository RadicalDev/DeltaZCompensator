import time
import math
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
from math import pi
from matplotlib import pyplot as plt
import random
from coordinates import get_points, sets
plt.ion()


class ZMapGenerator(object):
    def __init__(
            self,
            speed_max_travel=15000,
            speed_max_dot=9000,
            wait_time_home=5,
            wait_time_xyz_zero=5,
            wait_time_point=0.3,
            wait_time_row=5,
            z_height_row_change=15,
            r=65,
            step_size=10,
            csv_file="zmap.csv",
            printer=None,
            dial=None):

        self.r = r

        self.travel = speed_max_travel
        self.point_speed = speed_max_dot
        self.wth = wait_time_home
        self.wtz = wait_time_xyz_zero
        self.wtp = wait_time_point
        self.wtr = wait_time_row
        self.step_size = step_size
        self.z_height_row_change = z_height_row_change
        self.points = []
        self.points_adjusted = []
        self.csv_file = csv_file
        self.printer = printer
        self.dial = dial

        self.figure = None
        self.axes = None
        self.bbox = None
        self.background = None

        self.XY = None
        self.Z = None
        self.tree = None
        self.zmap = None

        self.left_right_horizontal_map = None
        self.right_left_horizontal_map = None
        self.up_down_vertical_map = None
        self.down_up_vertical_map = None
        self.diagonal_45_left_right_map = None
        self.diagonal_45_right_left_map = None
        self.diagonal_315_left_right_map = None
        self.diagonal_315_right_left_map = None

    def generate_circumference(self,n=100):
        points = sorted(list(set([(round(math.cos(2*pi/n*x)*self.r), round(math.sin(2*pi/n*x)*self.r)) for x in xrange(0,n+1)])))
        self.redraw(self.axes.scatter([x[0] for x in points], [y[1] for y in points], marker="+", color='red'))

    def generate_coordinates(self, plot=True):
        self.points = get_points(self.r, self.step_size)
        if plot:
            for x, y in self.points:
                self.redraw(self.axes.scatter(x, y, color='blue'))

    def redraw(self, points):
        self.axes.draw_artist(points)
        self.figure.canvas.blit(self.bbox)

    def main(self, use_computed_offsets=False, recompute_offsets=False, use_interp=False):
        self.points = []
        self.points_adjusted = []
        self.figure, self.axes = plt.subplots(1, 1)
        self.axes.set_aspect('equal')
        self.axes.set_xlim(-self.r-5, self.r+5)
        self.axes.set_ylim(-self.r-5, self.r+5)
        self.axes.hold(True)
        plt.show(False)
        plt.draw()
        self.bbox = self.axes.bbox
        self.background = self.figure.canvas.copy_from_bbox(self.bbox)
        self.generate_circumference()
        self.generate_coordinates()

        if use_computed_offsets or use_interp:
            self.load_zmap()

        if use_interp:
            self.generate_kdtree(*self.zmap)

        self.configure(use_computed_offsets=use_computed_offsets, recompute_offsets=recompute_offsets, use_interp=use_interp)

    def configure(self, use_computed_offsets=False, recompute_offsets=False, use_interp=False):
        self.printer.write("G28")
        time.sleep(self.wth)
        self.printer.write("G1 X0 Y0 Z0 F{0}".format(self.travel))
        time.sleep(self.wtz)
        z = 0

        mode = 'w'
        if use_computed_offsets and not recompute_offsets:
            mode = 'r'

        for s, desc in sets:
            map_file_name = "{0}_{1}.csv".format(self.csv_file, desc)
            print "Working on: ", map_file_name
            with open(map_file_name, mode) as f:
                n_points = len(self.points)
                current_point = 0
                top_time = time.time()
                bottom_time = time.time()
                time_taken = 0
                for x, y in s(self.points):
                    current_point += 1
                    time_taken = bottom_time-top_time
                    top_time = time.time()

                    print "Working on point {0} of {1} ({2} minutes left)".format(current_point, n_points, (time_taken*(n_points-current_point))/60.0)
                    # if use_interp:
                    #     z = -self.get_z_offset_kdtree(x, y)
                    #     print "Z Offset from KDTree: ", z
                    #
                    # elif use_computed_offsets:
                    #     z = -self.get_z_offset_literal(x, y)
                    #     print "Z Offset From Map: ", z

                    gcode = "G1 S1 X{0} Y{1} Z{2} F{3}"
                    gcode_go = gcode.format(x, y, 0, self.point_speed)
                    self.printer.write(gcode_go)
                    time.sleep(self.wtp)
                    measurement = self.dial.read()

                    # if recompute_offsets:
                    #     while measurement < -0.01 or measurement > 0.01:
                    #         old_z = z
                    #         if measurement < 0:
                    #             z = z + abs(measurement)
                    #         else:
                    #             z = z - abs(measurement)
                    #         print "{0} -> {1}".format(old_z, z)
                    #         gcode_go = gcode.format(x, y, 15, self.point_speed)
                    #         print "PRINTER GO UP: ", gcode_go
                    #         self.printer.write(gcode_go)
                    #         gcode_go = gcode.format(x, y, z, self.point_speed)
                    #         print "PRINTER GO DOWN: ", gcode_go
                    #         self.printer.write(gcode_go)
                    #         time.sleep(self.wtp)
                    #         measurement = self.dial.read()
                    #         print "Did it work? ", measurement
                    #     measurement = z

                    print "X: {0}, Y: {1}, Z: {2}, M: {3}".format(x, y, z, measurement)
                    if not use_computed_offsets or recompute_offsets:
                        f.write("{0},{1},{2}\n".format(x, y, measurement))
                    self.modify_point(x, y, color='orange')
                bottom_time = time.time()

        gcode = "G28"
        self.printer.write(gcode)

    def modify_point(self, x, y, marker='o', color='orange'):
        self.redraw(self.axes.scatter(x, y, marker=marker, color=color))

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

    def generate_buildplate_image_from_zmap(self):
        xyz = zip(*self.zmap)
        for x, y, z in xyz:
            self.points_adjusted.append([x, y, z])
        self.generate_buildplate_image()

    def generate_buildplate_image(self):
        plt.close()
        plt.ioff()

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        fig = plt.figure(figsize=plt.figaspect(0.3))
        ax1 = fig.add_subplot(121, projection='3d')

        x = [x[0] for x in self.points_adjusted]
        y = [y[1] for y in self.points_adjusted]
        z = [z[2] for z in self.points_adjusted]

        # ax.set_ylim(-self.r-5, self.r+5)
        # ax.set_xlim(-self.r-5, self.r+5)
        ax1.set_zlim(0, 3*max(z))

        surf = ax1.plot_trisurf(x, y, z, cmap=cm.jet)
        fig.colorbar(surf, shrink=0.5, aspect=10)

        ax2 = fig.add_subplot(122, projection='3d')
        ax2.plot_wireframe(x, y, z)

        plt.show()

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

    def get_z_offset_kdtree(self, x, y):
        xy = np.array([x,y])
        distances, indices = self.tree.query(xy, k=6)
        z_vals = self.Z[indices]
        delta_z = np.average(z_vals, weights=[(0.001/j) if j else 1 for j in distances])
        if not delta_z:
            delta_z = 0.00
        return delta_z
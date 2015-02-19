__author__ = 'jfindley'
import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.interpolate import interp1d

def generate_buildplate_image(points):

    fig = plt.figure(figsize=plt.figaspect(0.3))
    ax1 = fig.add_subplot(121, projection='3d')

    x = [x[0] for x in points]
    y = [y[1] for y in points]
    z = [z[2] for z in points]

    # ax.set_ylim(-self.r-5, self.r+5)
    # ax.set_xlim(-self.r-5, self.r+5)
    ax1.set_zlim(0, 3*max(z))

    surf = ax1.plot_trisurf(x, y, z, cmap=cm.jet)
    fig.colorbar(surf, shrink=0.5, aspect=10)

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_wireframe(x, y, z)

    plt.show()

def get_points(fn):
    points = []
    with open(fn, 'r') as f:
        for line in f:
            points.append([float(x) for x in line.strip().split(",")])
    return points

points_left = "../csv/zmap_5mm_r75_multi_left.csv"
points_right = "../csv/zmap_5mm_r75_multi_right.csv"
points_up = "../csv/zmap_5mm_r75_multi_up.csv"
points_down = "../csv/zmap_5mm_r75_multi_down.csv"
points_45_left = "../csv/zmap_5mm_r75_multi_45_left.csv"
points_45_right = "../csv/zmap_5mm_r75_multi_45_right.csv"
points_315_left = "../csv/zmap_5mm_r75_multi_315_left.csv"
points_315_right = "../csv/zmap_5mm_r75_multi_315_right.csv"

point_sets = [
    (points_left, 'left'),
    (points_right, 'right'),
    (points_up, 'up'),
    (points_down, 'down'),
    (points_45_left, '45 left'),
    (points_45_right, '45 right'),
    (points_315_left, '315 left'),
    (points_315_right, '315 right'),
][::-1]


bwar = {}
figure, axes = plt.subplots(2, 4, subplot_kw={'projection':'3d'})
for row in axes:
    for column in row:
        ax = column
        pfile, title = point_sets.pop()

        points = get_points(pfile)

        for point in points:
            xy = (point[0], point[1])
            if not xy in bwar:
                bwar[xy] = []
            bwar[xy].append(point[2])

        x = [x[0] for x in points]
        y = [y[1] for y in points]
        z = [z[2] for z in points]

        ax.set_title(title)
        ax.set_zlim(0, 3*max(z))
        surf = ax.plot_trisurf(x, y, z, cmap=cm.jet)
plt.show()

points_averaged = []
for key, value in bwar.iteritems():
    x, y = key
    z = value
    zx = range(-len(z)/2, len(z)/2)
    zy = z
    dz = interp1d(zx, zy, kind='cubic')(sum(z)/len(z))
    print sum(z)/len(z)
    points_averaged.append((x, y, dz))

generate_buildplate_image(points_averaged)
plt.show()


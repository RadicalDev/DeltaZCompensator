__author__ = 'jfindley'
import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
import time


def redraw(fig, bbox, ax, points):
    ax.draw_artist(points)
    fig.canvas.blit(bbox)


def modify_point(fig, ax, bbox, x, y, marker='o', color='orange'):
    redraw(fig, bbox, ax, ax.scatter(x, y, marker=marker, color=color))


def get_points(d, point_spacing=1):
    l = []
    for x in range(-d, d, point_spacing):
        for y in range(-d, d, point_spacing):
            if x**2 + y**2 <= (d**2):
                l.append((x, y))
    return l


def down_up_vertical(p):
    return sorted(p)


def up_down_vertical(p):
    return sorted(p)[::-1]


def left_right_horizontal(p):
    return sorted(p, key=lambda y: -y[1])


def right_left_horizontal(p):
    return sorted(p, key=lambda y: -y[1])[::-1]


def diagonal_45_left_right(p):
    return sorted(p, key=lambda z: -(z[0]-z[1]))


def diagonal_45_right_left(p):
    return sorted(p, key=lambda z: -(z[0]-z[1]))[::-1]


def diagonal_315_left_right(p):
    return sorted(p, key=lambda z: z[0]+z[1])


def diagonal_315_right_left(p):
    return sorted(p, key=lambda z: z[0]+z[1])[::-1]

sets = [
    left_right_vertical,
    right_left_vertical,
    left_right_horizontal,
    right_left_horizontal,
    diagonal_45_left_right,
    diagonal_45_right_left,
    diagonal_315_left_right,
    diagonal_315_right_left,
]

if __name__ == "__main__":
    d = 10

    figure, axes = plt.subplots(1, 1)
    axes.set_aspect('equal')
    axes.hold(True)
    orig_points = get_points(d, point_spacing=1)
    for x, y in orig_points:
        axes.scatter(x, y)
    #axes.scatter([x[0] for x in orig_points], [y[1] for y in orig_points])
    plt.show(False)
    plt.draw()
    bbox = axes.bbox
    background = figure.canvas.copy_from_bbox(bbox)

    colors = ['orange', 'black']
    color_index = 0

    for s in sets:
        points = s(orig_points)
        for x, y in points:
            modify_point(figure, axes, bbox, x, y, color=colors[color_index])
            time.sleep(0.02)

        if color_index == 0:
            color_index = 1
        else:
            color_index = 0
    plt.show()
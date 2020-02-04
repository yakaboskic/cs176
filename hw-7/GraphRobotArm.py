from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

import numpy as np

from shapely.geometry import LineString

def plot_line(ax, ob, alpha=.7, color=None):
    x, y = ob.xy
    if color is not None:
        ax.plot(x, y, '-o', alpha=alpha, color=color, linewidth=3, solid_capstyle='round', zorder=2)
    else:
        ax.plot(x, y, '-o', alpha=alpha, linewidth=3, solid_capstyle='round', zorder=2)


def graph_workspace(workspace):
    fig = plt.figure(1, dpi=90)

    ax = fig.add_subplot(111)
    line = LineString(workspace.robot_arm.get_joint_coordinates())

    plot_line(ax, line)

    if workspace.obstacles is not None:
        patches = []
        for obstacle in workspace.obstacles:
            polygon = Polygon(np.array(list(obstacle.exterior.coords)), True)
            patches.append(polygon)
        colors = 100*np.random.rand(len(patches))
        p = PatchCollection(patches, alpha=.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)

    ax.set_title('Robot Arm')

    ax.set_xlim(-workspace.dim[0]/2, workspace.dim[0]/2)
    ax.set_ylim(-workspace.dim[1]/2, workspace.dim[1]/2)

    return fig

def animate_workspace(workspace, path):
    fig = plt.figure(1, dpi=90)

    ax = fig.add_subplot(111)
    for i, state in enumerate(path):
        if i == 0 or i == len(path)-1:
            alpha = 1
        else:
            alpha = .4
        workspace.robot_arm.set_joint_angles(state)
        line = LineString(workspace.robot_arm.get_joint_coordinates())
        plot_line(ax, line, alpha=alpha, color='blue')

    if workspace.obstacles is not None:
        patches = []
        for obstacle in workspace.obstacles:
            polygon = Polygon(np.array(list(obstacle.exterior.coords)), True)
            patches.append(polygon)
        colors = 100*np.random.rand(len(patches))
        p = PatchCollection(patches, alpha=.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)

    ax.set_title('Robot Arm Animation')

    ax.set_xlim(-workspace.dim[0]/2, workspace.dim[0]/2)
    ax.set_ylim(-workspace.dim[1]/2, workspace.dim[1]/2)


def animate_workspace_2(workspace, path):
    fig = plt.figure(1, dpi=90)
    ax = plt.axes(xlim=(-workspace.dim[0]/2, workspace.dim[0]/2), ylim= (-workspace.dim[1]/2, workspace.dim[1]/2))
    line, = ax.plot([], [], '-o', alpha=.7, linewidth=3, solid_capstyle='round', zorder=2)

    if workspace.obstacles is not None:
        patches = []
        for obstacle in workspace.obstacles:
            polygon = Polygon(np.array(list(obstacle.exterior.coords)), True)
            patches.append(polygon)
        colors = 100*np.random.rand(len(patches))
        p = PatchCollection(patches, alpha=.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)

    ax.set_title('Robot Arm Animation')

    def init():
        workspace.robot_arm.set_joint_angles(path[0])
        ln = LineString(workspace.robot_arm.get_joint_coordinates())
        x, y = ln.xy
        line.set_data(x, y)
        return line,

    def animate(i):
        workspace.robot_arm.set_joint_angles(path[i])
        ln = LineString(workspace.robot_arm.get_joint_coordinates())
        x, y = ln.xy
        line.set_data(x, y)
        return line,

    ani = FuncAnimation(fig, animate, init_func=init, frames=len(path), interval=200, blit=True)

    return ani

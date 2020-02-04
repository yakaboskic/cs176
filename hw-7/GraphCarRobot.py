from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random
import numpy as np

from planar_display import TrajectoryView
from planar_trajectory import PlanarTrajectory
from planarsim import *

def graph_results(workspace, results, car_rrt, tree_plot=False):
    if tree_plot:
        fig = plot_tree(workspace, car_rrt)
        ax = plt.axes()
    else:
        fig = plt.figure(1, dpi=90, figsize=(8, 4.5))
        fig.tight_layout()

        ax = fig.add_subplot(111)
    #ax = plt.axes()
    if workspace.obstacles is not None:
        patches = []
        for obstacle in workspace.obstacles:
            polygon = Polygon(np.array(list(obstacle.exterior.coords)), True)
            patches.append(polygon)
        colors = 100*np.random.rand(len(patches))
        p = PatchCollection(patches, alpha=.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)

    control_sequence = []
    control_time = []
    for node in results[1:]:
        control_sequence += node.trajectory.sequence
        control_time += node.trajectory.durations

    total_traj = PlanarTrajectory(controls_rs, results[0].state[0],
                                  results[0].state[1],
                                  results[0].state[2],
                                  control_sequence,
                                  control_time)
    print('Length of Trajectory:', total_traj.calculate_trajectory_length())
    tview = TrajectoryView(total_traj)


    tview.draw(ax, sum(total_traj.durations) - .0001)

    return ax

def plot_tree(workspace, car_rrt):
    fig = plt.figure(1, dpi=90, figsize=(8, 4.5))
    fig.tight_layout()

    ax = fig.add_subplot(111)
    if workspace.obstacles is not None:
        patches = []
        for obstacle in workspace.obstacles:
            polygon = Polygon(np.array(list(obstacle.exterior.coords)), True)
            patches.append(polygon)
        colors = 100*np.random.rand(len(patches))
        p = PatchCollection(patches, alpha=.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)

    for node in car_rrt.vertices:
        ax.plot(node.state[0], node.state[1], 'o', color='blue', alpha=.5)

    return fig

def animate_results(workspace, results, car_rrt, tree_plot=False):
    if tree_plot:
        fig = plot_tree(workspace, car_rrt)
    else:
        fig = plt.figure(1, dpi=90, figsize=(8, 4.5))
        fig.tight_layout()

    ax = plt.axes()

    if workspace.obstacles is not None:
        patches = []
        for obstacle in workspace.obstacles:
            polygon = Polygon(np.array(list(obstacle.exterior.coords)), True)
            patches.append(polygon)
        colors = 100*np.random.rand(len(patches))
        p = PatchCollection(patches, alpha=.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)

    time_step = .05
    control_sequence = []
    control_time = []
    for node in results[1:]:
        control_sequence += node.trajectory.sequence
        control_time += node.trajectory.durations

    total_traj = PlanarTrajectory(controls_rs, results[0].state[0],
                                  results[0].state[1],
                                  results[0].state[2],
                                  control_sequence,
                                  control_time)

    #fig = plt.figure(figsize=(8, 4.5))
    #ax = plt.axes()

    def animate(i):
        #ax.clear()
        ax.set_xlim(-3, workspace.dim[0])
        ax.set_ylim(-3, workspace.dim[1])
        ax.set_aspect('equal')

        tview = TrajectoryView(total_traj)
        tview.draw(ax, i * .05)
        #print(f"hello: {i}")

    num_frames = int(total_traj.end_time / time_step)
    anim = FuncAnimation(fig, animate, frames=num_frames, interval=10, repeat=False)

    return anim

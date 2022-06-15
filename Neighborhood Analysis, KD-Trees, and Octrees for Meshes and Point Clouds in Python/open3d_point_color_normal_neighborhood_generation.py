import numpy as np
import open3d as o3d
import pandas as pd
import os

from scipy.spatial import KDTree
import matplotlib.pyplot as plt

# Downsampling function, using the voxel down sampling from Open3D, which inputs a point cloud and outputs arrays containing points, colors, normals
# There is no checks to see if the point cloud has colors and normals so either ensure that your point cloud has them or add normal and pseudo color generation
def downsample(point_cloud, voxel_size=0.02):

    point_cloud = point_cloud.voxel_down_sample(voxel_size=voxel_size)

    points = np.asarray(point_cloud.points)
    colors = np.asarray(point_cloud.colors)
    normals = np.asarray(point_cloud.normals)

    return points,colors,normals

# Function to calculate KD-tree, closest neighbourhoods and edges between the points
def calculate_edges(metric, num_neighbours = 4):
    # Calculate the KD-tree of the selected feature space
    tree = KDTree(metric)
    # Query the neighbourhoods for each point of the selected feature space to each point
    d_kdtree, idx = tree.query(metric,k=num_neighbours)
    # Remove the first point in the neighbourhood as this is just the queried point itself
    idx= idx[:,1:]

    # Create the edges array between all the points and their closest neighbours
    point_numbers = np.arange(len(metric))
    # Repeat each point in the point numbers array the number of closest neighbours -> 1,2,3,4... becomes 1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4...
    point_numbers = np.repeat(point_numbers, num_neighbours-1)
    # Flatten  the neighbour indices array -> from [1,3,10,14], [4,7,17,23], ... becomes [1,3,10,4,7,17,23,...]
    idx_flatten = idx.flatten()
    # Create the edges array by combining the two other ones as a vertical stack and transposing them to get the input that LineSet requires
    edges = np.vstack((point_numbers,idx_flatten)).T

    return edges


# Create Open3D objects to contain the LineSet and output Point cloud for visualization purposes 
def build_objects(points,colors,edges):
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(edges)
    line_set.paint_uniform_color([1, 0, 0])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    return line_set, point_cloud

# Create the visualizer object, set the background to black and create a coordinate system.
# Add the output point cloud and line set
def visualize_objects( line_set, point_cloud, plot_description ):
    # Initialize a visualizer object
    vis = o3d.visualization.Visualizer()
    # Create a window, name it and scale it
    vis.create_window(window_name = plot_description, width=800, height=600)
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])

    vis.add_geometry(point_cloud)
    vis.add_geometry(line_set)
    # Create a coordinate frame, set its size and origin position
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
    size=0.6,origin=(-1,-1,-1))
    vis.add_geometry(mesh_frame)
    # We run the visualizater
    vis.run()
    # Once the visualizer is closed destroy the window and clean up
    vis.destroy_window()


if __name__ == '__main__':

    # Load point cloud .ply into Open3D point cloud object
    point_cloud_path = os.path.join('point_cloud','duckStatue.ply')
    point_cloud_input = o3d.io.read_point_cloud(point_cloud_path)

    # Downsample
    points,colors,normals = downsample(point_cloud_input)
    # Calculate KD-tree / Edges - here you can change points to colors or normals to calculate their neighborhoods
    edges = calculate_edges(points, num_neighbours= 4)
    # Build objects - here you can change the points to normals or colors to show different features spaces and you can change the colors to color the feature space differently
    line_set, point_cloud_output = build_objects(points,colors,edges)
    # Visualzie objects
    visualize_objects(line_set,point_cloud_output,'Point Cloud with Distance Graph')

    
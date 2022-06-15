# Neighborhood Analysis, KD-Trees, and Octrees for Meshes and Point Clouds in Python

Code overview:

- open3d_animate_neighborhood_generation.py - **Open3D** code for visualizing the process of finding closest points and building neighborhoods of each point in a point cloud. The neighborhoods are shown as edges of a graph
- open3d_point_color_normal_neighborhood_generation.py - **Open3D** code for generating neighborhoods in Euclidian space, in color RGB space and in normal space. Each of these calculations is in a separate function and the visualization can be done in different combinations.
- open3d_octree_visualize.py - **Open3D** code for calculating and visualizing Octrees
- pyvista_neighborhood_distance_analysis.py - **PyVista** code for neighborhood distance analysis. Three examples are presented:
    - Simple function to demonstrate the built-in connectivity filter for thresholding a point cloud
    - Function to animate the rebuilding of a point cloud, one neighbourhood at a time, together with filtering out points
    - Function to interactively select with the mouse a point and calculate the points in its neighborhood, together with a slider for changing the size of the neighborhood
- vedo_neighborhood_distance_analysis.py - **Vedo** code for neighborhood analysis and the calculation of geodesic distance between two points on a mesh
    - Function to interactively select with the mouse a point, calculate the poits in its neighborhood, fit a circle on them and calculate and visualize their average normal
    - Function to interactively select two points on a mesh and calculate the geodesic distance between them, together with the shortest path between them

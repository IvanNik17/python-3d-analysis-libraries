import pyvista as pv
import os
import numpy as np
from scipy.spatial import KDTree

# Class for interactive voxelization of a mesh with different sizes voxel based on a GUI slider
class visualize_voxel_levels():
    # class initialization
    def __init__(self,mesh, plotter):
        self.plot = plotter
        self.mesh = mesh
    # Function for voxelization, which is called as a callback from the slider widget
    def voxelize_mesh(self, value):
        # The function gets the slider value as a input and calculates the voxel representation
        voxels = pv.voxelize(self.mesh, density=value, check_surface=False)
        # It then adds the voxels as a new mesh to the Plotter. Here it's important to not forget the name in the add_mesh,
        # as this tells PyVista that this is the same mesh so it does not create a new one each time
        self.plot.add_mesh(voxels, name='voxel_mesh', show_edges=True)
        return
    # Function for adding the widget to the Plotter and visualizing everything
    def show_different_voxel_levels(self):
        self.plot.camera_position = 'xy'
        # Create a widget give it the callback function, a minimum and maximum range, initial value, title and event type -
        # in our case it calls the callback function every time the widget slider is interacted with
        self.plot.add_slider_widget(self.voxelize_mesh, [0.01, 0.2], 0.01, title='Voxel Size', event_type = "always")
        self.plot.show()

# Function to calculate the radius of a sphere with an equal volume as a cube with a given side
def calculate_sphere_radius(voxel_size = 0.01):
    voxel_volume = voxel_size ** 3
    radius = ((3*voxel_volume)/(4*np.pi))**(1/3)
    return radius

# Function to generate density for each voxel and add it as a field
def calculate_neighbours(mesh, voxel_size = 0.01):
    # voxelize the given mesh with a specified size voxels
    voxels = pv.voxelize(mesh, density=voxel_size, check_surface=False)
    # Get the voxel center points
    voxel_centers = voxels.cell_centers().points
    # Get the mesh vertices
    mesh_vertices = mesh.points
    # Calculate the KDTree of the mesh vertices from Scipy
    kd_tree_vertices = KDTree(mesh_vertices)
    # Call the sphere radius function and calculate the new radius
    radius = calculate_sphere_radius(voxel_size)
    # Use the calculated KDTree and radius to get the neighbors for each voxel center
    neighbours = kd_tree_vertices.query_ball_point(voxel_centers,radius)
    # Count the number of points for each voxel center
    neighbour_count = [len(curr_neighbours) for curr_neighbours in neighbours]
    # Cast to array and normalize between 0 and 1 
    neighbour_count = np.array(neighbour_count, dtype=np.float32)
    neighbour_density =  neighbour_count/neighbour_count.max()
    # Add the density as a field to the voxels
    voxels['density'] = neighbour_density

    return voxels

# Function to visualize and threshold the voxel representation based on the calculated density
def visualize_thresh(voxels):
    p = pv.Plotter()
    p.camera_position = 'xy'
    p.add_mesh_threshold(voxels,show_edges=True)
    p.show()



if __name__ == '__main__':
    # Load the rooster statue mesh
    mesh_path = os.path.join('mesh','rooster.obj')
    mesh = pv.read(mesh_path)

    # Initialize the class and call the visualization function for voxel levels (comment next two lines if you want to run thresholding)
    vis_vox =  visualize_voxel_levels(mesh, pv.Plotter())
    vis_vox.show_different_voxel_levels()

    # # Get voxels and initialize thresholding visualization (comment next two lines if you want to run multi level interaction)
    # voxels = calculate_neighbours(mesh)
    # # Visualize thresholding
    # visualize_thresh(voxels)





    

import numpy as np
import open3d as o3d
import os

# Parameters class holding variables that change in the callback function
class params():
    # counter for the rotation
    counter = 0
    # counter for selecting a new voxel size
    sizes_counter = 0
    # array of voxel sizes between 0.01 and 0.1
    voxel_sizes = np.arange(0.01,0.1,0.005)
    # empty TriangleMesh object that will contain the cubes
    vox_mesh = o3d.geometry.TriangleMesh()
    # boolean value used for initial initialization of the voxel mesh
    initialize = True
    
# Callback function used to construct and rotate the voxel meshes
def rotate_and_change(vis):

    # When the counter is 0 generate the voxel grid and construct the voxel mesh
    if params.counter == 0:
        # generate the voxel grid using the voxel sizes setup in the params class
        voxel_grid=o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=params.voxel_sizes[params.sizes_counter])
        # get all voxels in the voxel grid
        voxels_all= voxel_grid.get_voxels()
        # geth the calculated size of a voxel
        voxel_size = voxel_grid.voxel_size
        # loop through all the voxels
        for voxel in voxels_all:
            # create a cube mesh with a size 1x1x1
            cube=o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
            # paint it with the color of the current voxel
            cube.paint_uniform_color(voxel.color)
            # scale the box using the size of the voxel
            cube.scale(voxel_size, center=cube.get_center())
            # get the center of the current voxel
            voxel_center = voxel_grid.get_voxel_center_coordinate(voxel.grid_index)
            # translate the box to the center of the voxel
            cube.translate(voxel_center, relative=False)
            # add the box to the TriangleMesh object
            params.vox_mesh+=cube
        
        # on the first run of the callback loop initialize the Triangle mesh by adding it to the Visualizer. In subsequent iterations just update the geometry
        if params.initialize:
            vis.add_geometry(params.vox_mesh)
            params.initialize = False
        else:
            vis.update_geometry(params.vox_mesh)


    # We create a 3D rotation matrix from x,y,z rotations, the rotations need to be given in radians
    R = params.vox_mesh.get_rotation_matrix_from_xyz((0, np.deg2rad(2), 0))
    # The rotation matrix is applied to the specified object - in our case the voxel mesh. We can also specify the rotation pivot center
    params.vox_mesh.rotate(R, center=(0, 0, 0))
    # tick the counter up
    params.counter+=1
    # For the changes to be seen we need to update both the geometry that has been changed and to update the whole renderer connected to the visualizer
    vis.update_geometry(params.vox_mesh)
    
    vis.update_renderer()

    # When the counter gets to 180 we zero it out. This is done because we rotate the mesh by 2 degrees on an iteration
    if params.counter >= 180:
        params.counter=0
        # we tick the voxel size counter
        params.sizes_counter +=1
        # if the voxel size counter becomes equal to the size of the voxel sizes array, reset it
        if params.sizes_counter >= len(params.voxel_sizes):
            params.sizes_counter=0
        # each time we clear the mesh. This is important, because without it we will just add more and more box primitives to the mesh object
        params.vox_mesh.clear()
  

    

# Read the bunny statue point cloud using numpy's loadtxt
point_cloud_path = os.path.join('point_cloud','bunnyStatue.txt')
point_cloud = np.loadtxt(point_cloud_path, delimiter=' ')
# Separate the into points, colors and normals array
points = point_cloud[:,:3]
colors = point_cloud[:,3:6]
normals = point_cloud[:,6:]

# Initialize a point cloud object
pcd = o3d.geometry.PointCloud()
# Add the points, colors and normals as Vectors
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)
pcd.normals = o3d.utility.Vector3dVector(normals)

# Create a voxel grid from the point cloud with a voxel_size of 0.01
# voxel_grid=o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=0.01)


# Initialize a visualizer object
vis = o3d.visualization.Visualizer()
# Create a window, name it and scale it
vis.create_window(window_name='Bunny Visualize', width=800, height=600)

# Add the voxel grid to the visualizer
# vis.add_geometry(voxel_grid)

# Register the callback function
vis.register_animation_callback(rotate_and_change)
# We run the visualizater
vis.run()
# Once the visualizer is closed destroy the window and clean up
vis.destroy_window()
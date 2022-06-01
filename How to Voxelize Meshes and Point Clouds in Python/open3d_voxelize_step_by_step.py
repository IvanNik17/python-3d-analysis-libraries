import numpy as np
import open3d as o3d
import os

# Helper parameters class containing variables that will change in the callback function
class params():
    # voxels counter that will stop the voxel mesh generation when there are no more voxels in the voxel grid
    counter = 0
    vox_mesh=o3d.geometry.TriangleMesh()

# Voxel builder callback function
def build_voxels(vis):
    # check if the counter is more than the amount of voxels
    if params.counter < len(voxels_all):
        # get the size of the voxels
        voxel_size = voxel_grid.voxel_size
        # create a box primitive of size 1x1x1
        cube=o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
        # paint the box uniformly with the color of the voxel
        cube.paint_uniform_color(voxels_all[params.counter].color)
        # scale the box to the size of the voxel
        cube.scale(voxel_size, center=cube.get_center())
        # get the center position of the current voxel
        voxel_center = voxel_grid.get_voxel_center_coordinate(voxels_all[params.counter].grid_index)
        # translate the box to the voxel center
        cube.translate(voxel_center, relative=False)
        # add the box primitive to the voxel mesh
        params.vox_mesh+=cube
        
        # on the first loop create the geometry and on subsequent iterations update the geometry
        if params.counter==0:
            vis.add_geometry(params.vox_mesh)
        else:
            vis.update_geometry(params.vox_mesh)

        # update the renderer
        vis.update_renderer()
        # tick up the counter
        params.counter+=1
    

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
voxel_grid=o3d.geometry.VoxelGrid.create_from_point_cloud(pcd,voxel_size=0.01)
# Get all the voxels in the voxel grid
voxels_all= voxel_grid.get_voxels()

# get all the centers and colors from the voxels in the voxel grid
all_centers=[]
all_colors=[]
for voxel in voxels_all:
    voxel_center = voxel_grid.get_voxel_center_coordinate(voxel.grid_index)
    all_centers.append(voxel_center)
    all_colors.append(voxel.color)
    

# Initialize a visualizer object
vis = o3d.visualization.Visualizer()
# Create a window, name it and scale it
vis.create_window(window_name='Bunny Visualize', width=800, height=600)
# Create a point cloud that will contain the voxel centers as points
pcd_centers = o3d.geometry.PointCloud()
# Tranform the numpy array into points for the point cloud 
pcd_centers.points = o3d.utility.Vector3dVector(all_centers)
# pcd_centers.colors = o3d.utility.Vector3dVector(all_colors)'
pcd_centers.paint_uniform_color([1, 0, 0])
# Add the voxel centers point cloud to the visualizer
vis.add_geometry(pcd_centers)

# Invoke the callback function
vis.register_animation_callback(build_voxels)
# We run the visualizater
vis.run()
# Once the visualizer is closed destroy the window and clean up
vis.destroy_window()



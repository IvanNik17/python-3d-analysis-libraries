from pyntcloud import PyntCloud
import os
import open3d as o3d

# Selection function which takes a name of the primitive and returns a mesh object
# For the sphere and torus we lower the default resolution values so they can be visualized easier
def choose_primitive(name):
    return {
        'box': o3d.geometry.TriangleMesh.create_box(),
        'cone': o3d.geometry.TriangleMesh.create_cone(),
        'sphere': o3d.geometry.TriangleMesh.create_sphere(resolution=5),
        'cylinder': o3d.geometry.TriangleMesh.create_cylinder(),
        'icosahedron': o3d.geometry.TriangleMesh.create_icosahedron(),
        'octahedron': o3d.geometry.TriangleMesh.create_octahedron(),
        'torus': o3d.geometry.TriangleMesh.create_torus( radial_resolution=10, tubular_resolution=5)
    }[name]

# Set up the path to the point cloud
point_cloud_path = os.path.join('point_cloud','bunnyStatue.txt')
# Load the point cloud. As internally from_file is calling Pandas, we set Pandas input parameters like separator, header and column names
cloud = PyntCloud.from_file(point_cloud_path, sep=" ", header=0, names=["x","y","z","r","g","b","nx","ny","nz"])

# We use the imported point cloud to create a voxel grid of size 64x64x64.
voxelgrid_id = cloud.add_structure("voxelgrid", n_x=64, n_y=64, n_z=64)
# We use the calculated occupied voxel grid ids to create the voxel representation of the point cloud
voxelgrid = cloud.structures[voxelgrid_id]
# We extract the density feature for each occupied voxel that we will use for coloring the voxels
density_feature_vector = voxelgrid.get_feature_vector(mode="density")
# Calculate the maximum density to normalize the colors
max_density = density_feature_vector.max()
# We extract the shape of a voxel, as well as the position of each point in X, Y, Z in the voxel grid
voxel_size = voxelgrid.shape
x_cube_pos = voxelgrid.voxel_x
y_cube_pos = voxelgrid.voxel_y
z_cube_pos = voxelgrid.voxel_z


# Initialize a open3d triangle mesh object
vox_mesh = o3d.geometry.TriangleMesh()


# go through all voxelgrid voxels
for idx in range(0, len(voxelgrid.voxel_n)):
    # get the id of the current voxel in the voxel grid
    curr_number = voxelgrid.voxel_n[idx]
    # get the center of the voxel grid voxel
    voxel_center = voxelgrid.voxel_centers[curr_number]
    # get the density value of the current voxel. Because the density matrix is in the shape X,Y,Z, where they are the coordinates in the voxel grid
    # we use the voxel grid positions we already
    curr_density = density_feature_vector[x_cube_pos[idx],y_cube_pos[idx],z_cube_pos[idx]]
    # we normalize the value using the maximum density
    curr_density_normalized = curr_density / max_density
    # create a box primitive in open3d
    # cube=o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
    primitive = choose_primitive('cylinder')
    # paint the box uniformly using the normalized density
    primitive.paint_uniform_color((curr_density_normalized,curr_density_normalized,curr_density_normalized))
    # scale the cube using the saved voxel size
    primitive.scale(voxel_size[0], center=primitive.get_center())
    # we translate the box to the center position of the voxel
    primitive.translate(voxel_center, relative=True)
    # add to the voxel mesh
    vox_mesh+=primitive


# Initialize a visualizer object
vis = o3d.visualization.Visualizer()
# Create a window, name it and scale it
vis.create_window(window_name='Bunny Visualize', width=800, height=600)
# add the voxel mesh to the visualizer
vis.add_geometry(vox_mesh)
vis.run()
# Once the visualizer is closed destroy the window and clean up
vis.destroy_window()

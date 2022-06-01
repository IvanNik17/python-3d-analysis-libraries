import trimesh
import numpy as np
import os
# Load the rooster mesh. Trimesh directly detects that the mesh is textured and contains a material
mesh_path = os.path.join('mesh','rooster.obj')
mesh = trimesh.load(mesh_path)

# Voxelize the loaded mesh with a voxel size of 0.01. We also call hollow() to remove the inside voxels, which will help with color calculation
angel_voxel = mesh.voxelized(0.01).hollow()

# Transform the texture information to color information, mapping it to each vertex. Transform it to a numpy array
only_colors = mesh.visual.to_color().vertex_colors
only_colors = np.asarray(only_colors)
# If we want to add the color information to the mesh uncomment this part
# mesh.visual = mesh.visual.to_color()

# Extract the mesh vertices
mesh_verts = mesh.vertices

# We use the ProximityQuery built-in function to get the closest voxel point centers to each vertex of the mesh
_,vert_idx = trimesh.proximity.ProximityQuery(mesh).vertex(angel_voxel.points)

# We initialize a array of zeros of size X,Y,Z,4 to contain the colors for each voxel of the voxelized mesh in the grid
cube_color=np.zeros([angel_voxel.shape[0],angel_voxel.shape[1],angel_voxel.shape[2],4])

# We loop through all the calculated closest voxel points
for idx, vert in enumerate(vert_idx):
    # Get the voxel grid index of each closets voxel center point
    vox_verts = angel_voxel.points_to_indices(mesh_verts[vert])
    # Get the color vertex color
    curr_color = only_colors[vert]
    # Set the alpha channel of the color
    curr_color[3] = 255
    # add the color to the specific voxel grid index 
    cube_color[vox_verts[0],vox_verts[1], vox_verts[2],:] = curr_color

# generate a voxelized mesh from the voxel grid representation, using the calculated colors 
voxelized_mesh = angel_voxel.as_boxes(colors=cube_color)

# Initialize a scene
s = trimesh.Scene()
# Add the voxelized mesh to the scene. If want to also show the intial mesh uncomment the second line and change the alpha channel of in the loop to something <100
s.add_geometry(voxelized_mesh)
# s.add_geometry(mesh)
s.show()
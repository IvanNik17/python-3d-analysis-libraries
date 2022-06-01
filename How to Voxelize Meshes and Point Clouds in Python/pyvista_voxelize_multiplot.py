import pyvista as pv
import os

# Load mesh and texture into PyVista
mesh_path = os.path.join('mesh','rooster.obj')
mesh = pv.read(mesh_path)
tex_path = os.path.join('mesh','rooster01.jpg')
tex = pv.read_texture(tex_path)

# Initialize the plotter object with four sub plots
pl = pv.Plotter(shape=(2, 2))
# First subplot show the mesh with the texture
pl.subplot(0, 0)
pl.add_mesh(mesh,name='rooster',texture = tex)

# Second subplot show the voxelized repsentation of the mesh with voxel size of 0.01. We remove the surface check as the mesh has small imperfections
pl.subplot(0, 1)
voxels = pv.voxelize(mesh, density=0.01, check_surface=False)
# We add the voxels as a new mesh, add color and show their edges
pl.add_mesh(voxels, color=True, show_edges=True)

# Third subplot shows the voxel representation using cones 
pl.subplot(1,0)
glyphs = voxels.glyph(factor=1e-3, geom=pv.Cone())
pl.add_mesh(glyphs)

# Forth subplot shows the voxels together with a contour showing the per voxel distance to the mesh
pl.subplot(1,1)
# Calculate the distance between the voxels and the mesh. Add the results as a new scalar to the voxels
voxels.compute_implicit_distance(mesh, inplace=True)
# Create a contour representing the calculated distance
contours = voxels.contour(6, scalars="implicit_distance")
# Add the voxels and the contour with different opacity to show both
pl.add_mesh(voxels, opacity=0.25, scalars="implicit_distance")
pl.add_mesh(contours, opacity=0.5, scalars="implicit_distance")


# Link all four views so all cameras are moved at the same time
pl.link_views()
# Set camera start position
pl.camera_position = 'xy'
# Show everything
pl.show()

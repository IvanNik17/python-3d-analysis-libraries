# How to Voxelize Meshes and Point Clouds in Python

Code overview:

- open3d_voxelize_multiple_levels.py - **Open3D** code for voxelization of the bunny statue with different sizes of voxel grids, transforming them into a mesh and animating them in real time
- open3d_voxelize_step_by_step.py - **Open3D** code for visualization of the voxel grid creation as an animation. The voxels are precomputed and then visualized in an animation callback
- pyntcloud_voxelize.py - **pyntcloud** code for voxelization of the bunny statue, calculating the voxel density and using different primitives instead of cubes, like spheres, cylinders, cones, etc.
- pyvista_voxelize_multiplot.py - **PyVista** code for creating a multiplot visualization of the rooster statue mesh, the voxelized version, a version with cones instead of cubes and a version that has pseudo-color map of the per voxel distances between mesh vertices and voxels
- pyvista_voxelize_widgets.py - **PyVista** code for creating two interactive widget examples - first an interactive voxel thresholding tool and second an interactive voxelization tool for choosing the size of the voxel grid.
- trimesh_voxelize.py - **Trimesh** code for creating a voxel representation of the rooster and calculating per voxel colors by mapping the texture information to the mesh vertices and calculating the closed distances between each voxel and mesh vertex. 


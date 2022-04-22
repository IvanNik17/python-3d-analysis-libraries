import numpy as np
import open3d as o3d

# Animation callback function. it needs to contain as a minimum the visualizer reference
def rotate_around(vis):
    # We create a 3D rotation matrix from x,y,z rotations, the rotations need to be given in radians
    R = mesh.get_rotation_matrix_from_xyz((0, np.deg2rad(2), 0))
    # The rotation matrix is applied to the specified object - in our case the mesh. We can also specify the rotation pivot center
    mesh.rotate(R, center=(0, 0, 0))

    # We create a 3D rotation matrix for the sphere as well in the opposite direction
    R_sphere = mesh.get_rotation_matrix_from_xyz((0, np.deg2rad(-4), 0))
    # Apply it
    sphere_mesh.rotate(R_sphere, center=(0, 0, 0))
    # For the changes to be seen we need to update both the geometry that has been changed and to update the whole renderer connected to the visualizer
    vis.update_geometry(mesh)
    vis.update_geometry(sphere_mesh)
    vis.update_renderer()

if __name__ == '__main__':

    print(o3d.__version__)

    # Load mesh, together with setting the flag for post-processing to True, so the texture and material will be loaded
    mesh_path = 'mesh/angelStatue_lp.obj'
    mesh = o3d.io.read_triangle_mesh(mesh_path,True)

    print(mesh)
    print('Vertices:')
    print(np.asarray(mesh.vertices))
    print('Triangles:')
    print(np.asarray(mesh.triangles))


    # We can extract information from the mesh like faces, UVs and texture
    mesh_faces = mesh.triangles
    mesh_uvs = mesh.triangle_uvs
    texture = mesh.textures



    # We create a visualizer object that will contain references to the created window, the 3D objects and will listen to callbacks for key presses, animations, etc.
    vis = o3d.visualization.Visualizer()
    # New window, where we can set the name, the width and height, as well as the position on the screen
    vis.create_window(window_name='Angel Visualize', width=800, height=600)

    # We call add_geometry to add a mesh or point cloud to the visualizer
    vis.add_geometry(mesh)

    # We can easily create primitives like cubes, sphere, cylinders, etc. In our case we create a sphere and specify its radius
    sphere_mesh = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)

    # We can compute either vertex or face normals
    sphere_mesh.compute_vertex_normals()
    # Add the sphere to the visualizer
    vis.add_geometry(sphere_mesh)
    # Translate it from the center
    sphere_mesh.translate((1, 0, 0))

    # We can register callback animation functions that will be run on every update cycle
    vis.register_animation_callback(rotate_around)
    # We run the visualizater
    vis.run()
    # Once the visualizer is closed destroy the window and clean up
    vis.destroy_window()

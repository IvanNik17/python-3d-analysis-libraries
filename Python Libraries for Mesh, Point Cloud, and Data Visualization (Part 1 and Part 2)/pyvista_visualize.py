import pyvista as pv
from pyvistaqt import BackgroundPlotter

# Function for updating the positions of the meshes and light in the update loop as a callback
def update_scene():
    # PyVista has simplified rotation methods for each rotation direction or you call call the rotate method and explicitly specify all rotations
    # We call inplace=True to update the changes to the mesh directly
    mesh.rotate_y(10,inplace=True)
    sphere.rotate_y(-10,inplace=True)
    
    # As the light object does not contain a rotate method, we just update its position based on the sphere.center position. 
    # The position method can both get and set the light position.
    light.position = sphere.center
    # We update the whole plotter
    p.update()

if __name__ == '__main__':
    # Load the mesh or point cloud if required
    mesh_path = 'mesh/angelStatue_lp.obj'
    mesh = pv.read(mesh_path)
    # if the mesh has a texture, it needs to be loaded separetely using read_texture
    tex_path = 'mesh/angelStatue_lp.jpg'
    tex = pv.read_texture(tex_path)

    # We create a plotter for non-blocking visualization, using pyvistaqt. If we don't need interactivity or animations we can just call pyvista.Plotter
    p = BackgroundPlotter(window_size=(600,400))
    
    # We set the camera position to be in the xy plane 
    p.camera_position = 'xy'
    # We set the front and back clipping planes
    p.camera.clipping_range = (0, 10)

    # We create the sphere which will orbit the angel statue and set its radius and center
    sphere = pv.Sphere(radius = 0.2, center=(0, 0, 1))

    # We create a blue point light at the position of the sphere
    light = pv.Light((0, 0, 1), (0, 0, 0), 'blue')

    # We add the angel statue mesh together with its texture to the plotter
    p.add_mesh(mesh,name='angel',texture = tex)
    # We add the sphere to the plotter. Just to demonstrate that PyVista supports the pbr rendering from VTK we make the sphere metallic.
    # If you get an error here your VTK version is <9.0. Either remove the pbr value or upgrade.
    p.add_mesh(sphere, pbr=True, metallic=0.7, roughness=0.2, diffuse=1)
    # We add the light to the plotter
    p.add_light(light)

    # We create a callback for the plotter and we set the function that will be run in the update loop. We also set the interval of the update
    # It is important to set the interval explicitly.
    p.add_callback(update_scene, interval=100)

    # We show the plotter and call p.app.exec_(), so the plotter stays open. This is important when running the pyvistaqt plotter.
    # If your visualization automatically closes add the last line
    p.show() 
    p.app.exec_()


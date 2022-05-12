import numpy as np
from plotoptix import TkOptiX
from plotoptix.materials import m_diffuse, m_clear_glass
import os

'''
PlotOptix contains two types of update callback functions. on_scene_compute is executed first and contains all CPU bound computations.
On the other hand on_rt_completed is executed after the ray tracing part is finished. It is used to update the scene visuals on the GPU.
Both updates can be paused, resumed and stopped individually.
'''
# ray tracing function update
def update_scene(rt: TkOptiX) -> None:
    # rotate the angel statue, specify the rotation in X,Y,Z in radians. If the center of rotation is not specified, then the center of the geometry is used
    rt.rotate_geometry("angel_mesh",(0, params.statue_angle, 0))
    # as the light does not have a rotate_geometry method we use the update_light method and give it a new position, we calculate the position in the on_scene_compute function
    rt.update_light("light2",pos = params.pos_light)
    # rotate the cube around itself in all three directions
    rt.rotate_geometry("cube",(params.cube_angle_self, params.cube_angle_self, params.cube_angle_self))
    # rotate the cube around the 0,0,0 center
    rt.rotate_geometry("cube",(0, params.cube_angle_around, 0), center=[0,0,0])

# cpu execution callback
def compute_changes(rt: TkOptiX, delta: int) -> None:
    # decrement the counter
    params.t -= params.delta_t
    # calculate the new position in X,Y,Z for the light
    params.pos_light = [np.sin(params.t), 0, np.cos(params.t)]

# class that contains all the used variables in the two callback functions
class params:
    pos_light = [0, 0, 1]
    t = 0
    delta_t = 0.2
    statue_angle = np.deg2rad(5)
    cube_angle_self = np.deg2rad(5)
    cube_angle_around = np.deg2rad(10)


# Paths to the angel mesh and texture
mesh_path = os.path.join('mesh','angelStatue_lp.obj')
texture_path = os.path.join('mesh','angelStatue_lp.jpg')

# setup the plotoptix visualizer and give it the callback functions
rt = TkOptiX(on_scene_compute=compute_changes, on_rt_completed=update_scene)

'''
Setup initial parameters:
    - the min_accumulation_step gives how many frames should be accumulated before the scene is shown - the higher the number the slower the visualization will be
    but it will loop better
    - max_accumulated_step gives the maximum frames for the scene
    - light_shading - gives how the scene will look - 'Soft' is faster, but 'Hard' is better when there is transparency, subsurface scattering, etc.
'''
rt.set_param(min_accumulation_step=30,
            max_accumulation_frames=512,
            light_shading="Hard")

# set the background color
rt.set_background(0)
# set the ambient lighting
rt.set_ambient(0.25)
# set how long will be the tracing distance for the shot rays. Higher values make the visualization slower, but make glass, transparent, etc. shaders look better
rt.set_uint("path_seg_range", 15, 40)
# set what will be visualized at places where a ray does not intersect with anything. In our case ambient and volume gives better results for volumetric scattering
rt.set_background_mode("AmbientAndVolume")

# Load the angel statue texture and setup the defuse color texture to it. In our case we have one object with one texture and we can do this
# If we had more objects with texture, then each needs to be instantiated from the diffuse shader material
rt.load_texture("angel", texture_path)
m_diffuse["ColorTextures"] = [ "angel" ]
# Update the diffuse material with the texture
rt.update_material("diffuse", m_diffuse)
# Load the mesh, give it a name and material
rt.load_merged_mesh_obj(mesh_path,mesh_name = "angel_mesh",c=0.92)

# setup a clear glass material for the cube object, give it initial position, u,v,w scales of its sides and give it the glass material
rt.setup_material("glass", m_clear_glass)
rt.set_data("cube", pos=[0, -0.5, 1], u=[0, 0.9, 0], v=[0, 0, 0.9],w=[0.1, 0, 0], c=np.array([0.9, 0.7, 0.7]), geom="Parallelepipeds", mat="glass")
 
# setup a simple camera
rt.setup_camera("cam1")

# create a light with a position in the origin and white color for boosting the clarity of the mesh
rt.setup_light("light1", color=2, radius=2)

# create the rotating light. The color of the light is a combination of the color and intensity, so we create a separate light_power variable
# in_geometry makes the light an object that can be seen. And give it a radius.
light_power = 20
rt.setup_light("light2",color = np.array([0,0,1*light_power]), radius = 0.1, pos= np.array([2,0,1]), in_geometry=True)

# Add post-processing effects Gamma correction and Denoising
rt.add_postproc("Gamma")      # apply gamma correction postprocessing stage, or
rt.add_postproc("Denoiser")  # use AI denoiser (exposure and gamma are applied as well)


rt.start()
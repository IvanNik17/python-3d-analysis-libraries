from simple_3dviz import TexturedMesh
from simple_3dviz.window import show
from simple_3dviz.behaviours.misc import LightToCamera
from simple_3dviz.behaviours.movements import RotateModel,RotateRenderables
from simple_3dviz.renderables.textured_mesh import Material
from simple_3dviz import Spherecloud

import numpy as np

mesh_path = 'mesh/angelStatue_lp.obj'
texture_path = 'mesh/angelStatue_lp.jpg'

# Loading the mesh without a texture first
mesh = TexturedMesh.from_file(mesh_path)
# Create a material and load the texture to it. Set visual properties to the material
mtl = Material.with_texture_image(texture_path, ambient=(0.4, 0.4, 0.4), diffuse=(0.4, 0.4, 0.4), specular=(0.1, 0.1, 0.1), Ns=2)
# Add the material to the mesh
mesh.material = mtl


# Create the position of the single point in a point cloud that will represent the sphere
rotating_point_pos = np.expand_dims(np.array([0,0,1]), axis=0)
# Generate the point cloud point with a larger size and a specified color
point = Spherecloud(rotating_point_pos, sizes = 0.1,colors=(0,0,1))

# Call the show function and create the animation directly in it
'''
First create the visualizer and add the mesh and sphere to it
Then in the behaviours list we setup the Light to the camera
Because in Simple-3dviz the point clouds do not have an explicit rotation function we call RotateModel to rotate all the objects in the scene in a specified direction
Second because we want the mesh to rotate in the opposite direction we call RotateRenderables, we add the mesh, axis and speed in the other direction.
This is a bit of hacky implementation but it produces the required results. Another way to do it is if we don't use a point cloud for the sphere
Finally we position the camera, setup the up vector, change the background and setup the size of the window
'''
show([mesh,point],
    behaviours=[LightToCamera(),
    RotateModel(axis='y', speed = np.deg2rad(2)),
    RotateRenderables([mesh],axis=[0, 1.0, 0], speed = np.deg2rad(4))],
    camera_position=(0, 0, 3),
    up_vector=(0, 1, 0),
    background=(0, 0, 0, 1),
    size=(600, 600)  
)


import numpy as np
import trimesh 
import pyrender
import os
import time

# Angel mesh path
mesh_path = os.path.join('mesh','angelStatue_lp.obj')
# Initialize the Pyrender scene with a specific ambient light and background color
scene = pyrender.Scene(ambient_light=[0.02, 0.02, 0.02],bg_color=[0.0, 0.0, 0.0])
# Load the angel statue using Trimesh and transform it into a Pyrender object
mesh = trimesh.load(mesh_path)
mesh = pyrender.Mesh.from_trimesh(mesh)
# Create a sphere used together with the light to rotate around the angel. We use the Trimesh primitives
light_point = trimesh.creation.uv_sphere(radius=0.1)
# Create a metallic roughness material for the sphere with a specific base color
mat_metal = pyrender.MetallicRoughnessMaterial('metal',metallicFactor=0.8,roughnessFactor=0.4, baseColorFactor=(0,0,255,1))
# Transform the Trimesh primitive into a Pyrender object
light_point = pyrender.Mesh.from_trimesh(light_point, material = mat_metal)
# Create a box primitive in Trimesh, scale and transform it into a Pyrender object
surface = trimesh.creation.box(extents=(3,0.2,3))
surface= pyrender.Mesh.from_trimesh(surface)
# Initialize a point light with a specific color and intensity
light = pyrender.PointLight(color=[0.0, 0.0, 1.0], intensity=10.0)
# Initialize a perspective camera with a specific field of view and aspect ratio
cam = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.414)

# Set the 4x4 transformation matrices for the camera and the box surface. Start with an eye matrix and change the translation
cam_matrix = np.eye(4)
cam_matrix[:3, 3] = np.array([0,0,3])

surface_matrix = np.eye(4)
surface_matrix[:3, 3] = np.array([0,-1,0])

# Create a node for the angel mesh, the light, the ball, camera and box
nm = pyrender.Node(mesh=mesh, matrix=np.eye(4))
nl = pyrender.Node(light=light, matrix=np.eye(4))
nlp = pyrender.Node(mesh=light_point, matrix=np.eye(4))
nc = pyrender.Node(camera=cam, matrix=cam_matrix)
ns = pyrender.Node(mesh=surface, matrix=surface_matrix)

# Add all the nodes to the scene
scene.add_node(nm)
scene.add_node(nl)
scene.add_node(nc)
scene.add_node(nlp)
scene.add_node(ns)

# Create a Pyrender viewer. The viewer can take two dictionaries - one for viewer_flags and one for render_flags. We show how these can be made
viewer_options = {"rotate_axis": [0,1,0]}
render_options = {"face_normals":False}
# We explicitly set raymond lighting - aka connected to the camera and set the flag for running the viewer in a separate thread so we can animate the objects
v = pyrender.Viewer(scene, use_raymond_lighting = True, viewer_flags = viewer_options, render_flags = render_options, run_in_thread=True )

# Create a light 4x4 transformation matrix that will be changed in the loop
light_matrix = np.eye(4)

# a loop that is active until the viewer is active
while v.is_active:
    # acquire the renderer and stop it to change the objects
    v.render_lock.acquire()

    # get the delta of time
    delta_change = time.time()

    # calculate the X, Y, Z positions of the light
    xpos = np.sin(-delta_change*2)
    ypos = np.sin(delta_change*3) * np.cos(delta_change*3)
    zpos = np.cos(-delta_change*2)
    # set them in the translation part of the transformation matrix
    light_matrix[:3, 3] = np.array([xpos,ypos,zpos])

    # leverage the Trimesh tranformation rotation_matrix method to create the rotation around the Y axis for the angel statue
    yaxis = [0,1,0]
    R = trimesh.transformations.rotation_matrix(delta_change*2, yaxis)

    # We use the method for setting a new position/rotation of the object set_pos, which takes the name of the node and a transformation matrix
    scene.set_pose(nl, light_matrix)
    scene.set_pose(nlp, light_matrix)
    scene.set_pose(nm, R)
    # We release the lock of the renderer so it can update the objects
    v.render_lock.release()

    # We call sleep for a short period so the results can be visualized
    time.sleep(0.01)


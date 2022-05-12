import numpy as np
import trimesh
import pyrender
import pandas as pd

'''
Pandas data pre-processing
'''
# Load the csv data
dataset_path = 'dataset\metadata.csv'
dataset = pd.read_csv(dataset_path)  

# Transform the DateTime column to pandas datetime
dataset_scatter = dataset[['Temperature','Humidity','Wind Speed']].to_numpy()
# Calcualte the mean point of the dataset for positioning the camera later
dataset_scatter_mean = dataset_scatter.mean(axis=0)
# We select to visualize the wind direction for each point as a capsule primitive rotated around the world Y axis
yaxis = [0,1,0]
# Go through all rows of the dataframe and calculate the transformation matrix using the trimesh.transformations method. It returns a 4x4 matrix with the rotation part calculated
all_rots = []
for index, row in dataset.iterrows():
    all_rots.append(trimesh.transformations.rotation_matrix(np.deg2rad(row['Wind Direction']), yaxis))
all_rots = np.array(all_rots)

'''
Pyrender generate objects and visualize
'''

# Initialize the scene, give it an ambient light and background color
scene = pyrender.Scene(ambient_light=[0.02, 0.02, 0.02],bg_color=[0.0, 0.0, 0.0])

# Create a Trimesh uv_sphere object and give it a specific color
uv_sphere = trimesh.creation.uv_sphere(radius=0.2)
uv_sphere.visual.vertex_colors = [1.0, 0.0, 0.0]
# Create 4x4 transformation matrices for each point in dataset
tfs = np.tile(np.eye(4), (len(dataset_scatter), 1, 1))
# Add the Temperature, Humidity, Wind Speed values from the dataset to the translation part of the 4x4 matrix for each point
tfs[:,:3,3] = dataset_scatter
# Create a 'point cloud' in Pyrender by inputing the uv_sphere and the generated 4x4 transformations for all the points
sphere_scatter = pyrender.Mesh.from_trimesh(uv_sphere, poses=tfs)
# Create a mesh node and add it to the scene
ns = pyrender.Node(mesh=sphere_scatter)
scene.add_node(ns)

# Create a Trimesh capsule object and give it a specific radius, height and color
capsule_arrow = trimesh.creation.capsule(radius=0.1,height =0.5)
capsule_arrow.visual.vertex_colors = [0.0, 1.0, 0.0]
# Add the Temperature, Humidity, Wind Speed values from the dataset to the 4x4 transformation matrices created from the trimesh.transformations.rotation_matrix
# These 4x4 matrices already contain the rotation information from the Wind Direction
all_rots[:,:3,3] = dataset_scatter
# Create a 'point cloud' in Pyrender by inputing the capsule and the generated 4x4 transformations for all the points
capsule_scatter = pyrender.Mesh.from_trimesh(capsule_arrow, poses=all_rots)
# Create a mesh node and add it to the scene
nc = pyrender.Node(mesh=capsule_scatter)
scene.add_node(nc)

# Create a Pyrender perspective camera
cam = pyrender.PerspectiveCamera(name='main_cam', yfov=np.pi / 3.0, aspectRatio=1.414)
# Create a transformation matrix, add the moved dataset mean point as the translation part of this matrix
cam_matrix = np.eye(4)
cam_pos = dataset_scatter_mean
cam_pos[2] += 80
cam_matrix[:3, 3] = cam_pos
# Createa camera node at a specific position and add it to the scene
ncam = pyrender.Node(camera=cam, matrix=cam_matrix)
scene.add_node(ncam)

# Create the Pyrender viewer. As we are not creating explicit animations we don't need to run the viewer in another thread.
# We start the rotation by pressing the A button on the keyboard
viewer_options = {"rotate_axis": [0,1,0]}
v = pyrender.Viewer(scene, use_raymond_lighting=True, viewer_flags = viewer_options)


from matplotlib import colors
import numpy as np
from plotoptix import TkOptiX
from plotoptix.utils import map_to_colors  # feature to color conversion
from plotoptix.materials import m_clear_glass, m_mirror, m_plastic  # predefined materials
import os
import pandas as pd

# cpu execution callback
def compute_changes(rt: TkOptiX, delta: int) -> None:
    # calculate new position for the camera. Numbers are chosen heuristically, to make an interesting path and can be changed to create different movements
    params.eye = [40, 30 * np.cos(params.t) + 50, 40 * np.sin(params.t)]
    params.t += 0.05

# ray tracing function update
def update_scene(rt: TkOptiX) -> None:
    # the way to update the camera position and orientation is done through calling update_camera and giving it a new 4x4 transformation matrix. We only update the  X,Y,Z translation
    rt.update_camera(eye=params.eye)

# Simple class containing the initializations of the different variables used in the callback functions
class params:
    eye = [0, 0, 0]
    t = 0


'''
Pandas data pre-processing
'''
# Load the csv data
dataset_path = os.path.join('dataset','metadata.csv')
dataset = pd.read_csv(dataset_path)  
print(dataset.head())
# Select Temperature, Humidity and Dew Points to create a 3D plot and transform into numpy
dataset_scatter = dataset[['Temperature', 'Humidity','Dew Point']].to_numpy()


# Initialize the visualizer and set the on_scene_compute and on_rt_completed functions
rt = TkOptiX(on_scene_compute=compute_changes, on_rt_completed=update_scene)

# Set the parameters for accumulation of frames, in our case we use a very low number for min_accumulation_step because of the large number of particles representing the plot
# With a RTX card or when you do not need to create an animation you can use larger values and create a higher fidelity, less noisy plot
rt.set_param(min_accumulation_step=3, max_accumulation_frames=30,light_shading="Hard")
# setup the background and ambient light
rt.set_background(0.1)
rt.set_ambient(0.2) 
# Initialize the three used prebuild materials for glass, plastic and a mirror like surface
rt.setup_material("glass", m_clear_glass)
rt.setup_material("plastic", m_plastic)
rt.setup_material("mirror", m_mirror)
# Create a color map from the Temperature column, using the "seismic" colormap from matplotlib
colors = map_to_colors(dataset_scatter[:,0], 'seismic')

# Create Parallelepiped particles for each of the datapoints from the dataset, setup their radius and colors. We use a plastic material to give them a nice shine
rt.set_data("particles", pos=dataset_scatter, r=dataset_scatter[:,1]*0.01, c=colors, geom="Parallelepipeds", mat="plastic")
# Create two planes - one flat and one 3D for side and bottom planes and give them interesting materials. We rotate them accordingly
rt.set_data("plane", pos=[0, 20, -20], u=[0, 100, 0], v=[0, 0, 70], c=np.array([0.9, 0.7, 0]), geom="Parallelograms", mat="glass")
rt.set_data("plane2", pos=[0, 20, 40], u=[0, 100, 0], v=[0, 0, 10],w=[40, 0, 0], c=np.array([0.9, 0.7, 0.7]), geom="Parallelepipeds", mat="mirror")

# Setup a camera and choose the DoF type, which contains a depth of field effect
rt.setup_camera("cam",cam_type="DoF", eye=params.eye,up =[1,0,0])

# Create two lights at each side of the plot. We have selected the positons heuristically so the lights can give a 2 point lighting for the dataset
rt.setup_light("light1",pos=[40,120,0], color=np.array([0.1, 0.1, 0.1])*50, radius=13)
rt.setup_light("light2",pos=[40, 0,0], color=np.array([0.1, 0.1, 0.1])*50, radius=13)

# setup a coordinate system box. Currently PlotOptiX only has a simple box as a coordinate system around everything in the scene.
rt.set_coordinates(mode="Box")

# Setup visualizer options and post-processing effects
rt.set_background_mode("AmbientAndVolume")
rt.set_uint("path_seg_range", 15, 40)
rt.set_float("tonemap_exposure", 0.5)
rt.set_float("tonemap_gamma", 2.2)

rt.add_postproc("Gamma")      # apply gamma correction postprocessing stage, or
rt.add_postproc("Denoiser")  # use AI denoiser (exposure and gamma are applied as well)

rt.start()
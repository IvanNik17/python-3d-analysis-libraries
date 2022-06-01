import numpy as np
import polyscope as ps
import time
import math
import pandas as pd

# Simple class holding a counter variable, which will be used to select specific subset of the points to build edges between
class params:
    t = 2

# Callback function used for the animation
def callback():

    # Delta time used for rotation of the camera around the dataset
    delta_change = time.time()
    # set the X axis position
    xpos = 80*np.sin(-delta_change*0.5)
    # set the Z axis position
    zpos = 80*np.cos(-delta_change*0.5)
    # The way we set the camera position is by invoking the look_at method, giving it a new position of the camera and the target to look at
    # In our case the target is the mean point of the dataset
    ps.look_at((xpos+ dataset_scatter_mean[0], dataset_scatter_mean[1], zpos + dataset_scatter_mean[2]), dataset_scatter_mean)
    # Select  the subset of the datase to compute edges between. We use the t parameter for this
    dataset_scatter_temp = dataset_scatter[:params.t,:]
    # Make a range for the subset going from the first to the last element
    times = np.arange(0,len(dataset_scatter_temp))
    # Repeat each value in the range and reshape them so the go as 1-2, 2-3, 3-4, 4-5, etc. so the edges can be visualized
    edges = np.repeat(times, 2)
    edges = np.reshape(edges[1:-1], (-1, 2))

    # remove the old curve network so it can be redrawn
    if params.t!=2: ps.get_curve_network("dataset_curve").remove()
    # create a new curve network from the subset
    ps_net = ps.register_curve_network("dataset_curve", dataset_scatter_temp, edges)
    # add colors depending on the temperature and enable them
    ps_net.add_scalar_quantity("temperature_node", dataset_scatter_temp[:,0], enabled=True)

    # increment the counter t and if larger than the dataset size return to beginning
    params.t += 1
    if params.t >= len(dataset_scatter): params.t = 2


'''
Pandas data pre-processing
'''
# Load the csv data
dataset_path = 'dataset\metadata.csv'
dataset = pd.read_csv(dataset_path)  

# Transform the DateTime column to pandas datetime
dataset['DateTime']=  pd.to_datetime(dataset['DateTime'], format='%d/%m/%Y %H:%M')
# Select the temperature, humidity and widn speed columns and transform them into a numpy array
dataset_scatter = dataset[['Temperature','Humidity','Wind Speed']].to_numpy()
# Calculate the mean point of the dataset for positioning the camera
dataset_scatter_mean = dataset_scatter.mean(axis=0)

'''
Polyscope initialization and visualization
'''

# Initialize Polyscope visualizer
ps.init()

# Setup camera initial position
cam_pos = np.array([1,1,1])

# Register a point cloud based on all the scatter points
ps_cloud = ps.register_point_cloud("dataset_points", dataset_scatter)
# Create a scalar field in the point cloud object based on temperature column and scale it with a scalar
ps_cloud.add_scalar_quantity("temperature_size", dataset_scatter[:,0]*100)
# Set the scalar field as the radius of the points
ps_cloud.set_point_radius_quantity("temperature_size")
# Initialize the callback function
ps.set_user_callback(callback)
# Show the visualizer
ps.show()
# After we close the screen remove all callbacks
ps.clear_user_callback()
import numpy as np
import open3d as o3d
import pandas as pd

'''
Read and transform the dataframe
'''
#  Read the csv with the weather metadata with Pandas
dataset_path = 'dataset\metadata.csv'
dataset = pd.read_csv(dataset_path)  
print(dataset.head())

# Transform the DateTime column into a datetime format
dataset['DateTime']=  pd.to_datetime(dataset['DateTime'], format='%d/%m/%Y %H:%M')
# Extract only the months and multiply them by an arbitrary 10 factor for easier visualization and separation
dataset['Months'] = dataset['DateTime'].dt.month*10
# Transform the Temperature, Humidity and the new Months columns to a numpy array
dataset_scatter = dataset[['Temperature', 'Humidity','Months']].to_numpy()


'''
Visualize using Open3D
'''

# Initialize a visualizer object
vis = o3d.visualization.Visualizer()
# Create a window, name it and scale it
vis.create_window(window_name='Statistic Visualize', width=800, height=600)

# Initialize a point cloud object
pcd = o3d.geometry.PointCloud()
# Tranform the numpy array into points for the point cloud 
pcd.points = o3d.utility.Vector3dVector(dataset_scatter)
# Add the point cloud to the visualizer
vis.add_geometry(pcd)
# Get options for the renderer for visualizing the coordinate system and changing the background
opt = vis.get_render_option()
opt.show_coordinate_frame = True
opt.background_color = np.asarray([0.5, 0.5, 0.5])
# Get the camera controller
ctrl = vis.get_view_control()
# This time we rotate the camera around the points and update the renderer
while vis.poll_events():
    ctrl.rotate(5, 0)
    vis.update_renderer()


# We run the visualizater
vis.run()
# Once the visualizer is closed destroy the window and clean up
vis.destroy_window()

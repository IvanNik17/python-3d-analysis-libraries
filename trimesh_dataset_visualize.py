import numpy as np
import pandas as pd
import trimesh


# Load csv data using pandas
dataset_path = 'dataset\metadata.csv'
dataset = pd.read_csv(dataset_path)  
# transform the DateTime column to a datetime structure
dataset['DateTime']=  pd.to_datetime(dataset['DateTime'], format='%d/%m/%Y %H:%M')

# We group the temperature column and calculate the average value based on the monthly values of the DateTime column, using the freq="M" input
temperature_per_month = dataset.groupby(pd.PeriodIndex(dataset['DateTime'], freq="M"))['Temperature'].mean().reset_index()
only_avg_temps = temperature_per_month["Temperature"]

# We use the interpolate function present in trimes to create a color temperature to visualize the high and low temperatures
colors_temp = trimesh.visual.interpolate(only_avg_temps, color_map = 'seismic')

# offset for generation of the cylinders so we can also show the coordinate system
offset=2

'''
Visualize Data using Trimesh
'''

# For each month generate a cylinder object
month_cylinders = []
for index, item in temperature_per_month.iterrows():
    # initialize a 4x4 transformation matrix
    matrix = np.eye(4)
    
    # move the cylinder in X direction so they don't overlap
    matrix[0][3] = index
    # move the cylinder in Y direction first with the offset and then with half of the temperature value.
    # We do this because the generated cylinders are scaled from their center. This way we get a column chart with zero at the bottom
    matrix[2][3] = item[1]/2+offset
    # We genmerate the cylinder with a set radius, height equal to the temperature and transformation based on the set positional offsets
    cylinder_mesh = trimesh.primitives.Cylinder(radius=0.5,height=item[1], transform = matrix)
    # We color the cylinder based on the temperature
    cylinder_mesh.visual.face_colors = colors_temp[index]
    # We append it to a list of cylinders for visualization
    month_cylinders.append(cylinder_mesh)


# Create a trimesh scene and add all the cylinders
s = trimesh.Scene(month_cylinders)

# Show the scene, set background color, smooth rendering and visualize the 3D axis
s.show(background=[30,30,30,255], smooth = True, flags={'axis': True})


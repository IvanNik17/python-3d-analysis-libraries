import pyvista as pv
import numpy as np
import pandas as pd
import matplotlib
from pyvistaqt import BackgroundPlotter

# Update function called by the callback
def update_scene():
    # Update the camera's azimuth angle each update iteration
    pl.camera.azimuth += 5
    # We update the whole plotter
    pl.update()

# Load the csv data
dataset_path = 'dataset\metadata.csv'
dataset = pd.read_csv(dataset_path)  
print(dataset.head())

# Transform the DateTime column to pandas datetime
dataset['DateTime']=  pd.to_datetime(dataset['DateTime'], format='%d/%m/%Y %H:%M')
# Create a months column and multiply it by an arbitrary separation value for easier visualization
separation_factor = 10
dataset['Months'] = dataset['DateTime'].dt.month * separation_factor
# Transform the pandas dataframe into a numpy array so it can be used in PyVista
dataset_scatter = dataset[['Temperature', 'Humidity','Months']].to_numpy()

# Calculate the minimum humidity value, the mean temperature value and all the unique months that are seen in the dataset
# We calculate this so we can use them as position data for labels for each month
max_humidity = dataset["Humidity"].min()
mid_temperature = dataset["Temperature"].mean()
months_unique = dataset["Months"].unique()
# Generate the label positions by combining the unique months, with columns of of mean temperature and maximum humidity values.
# We generate them like this so all labels can have the same position and just change the height depending on the monthly value
label_points = np.vstack([np.ones_like(months_unique)*mid_temperature,
                        np.ones_like(months_unique)*max_humidity,
                        months_unique]).T
# Get the names of the represented months. We will use these for text on the labels
label_names = dataset['DateTime'].dt.month_name().unique().tolist()

# Initialize the plotter object
pl = BackgroundPlotter()
# Create the 3D point cloud from the selected dataset. We set render_points_as_sphere to visualize 3D spheres and setup scalars as the "Temperature" to get color to each point
actor = pl.add_points(dataset_scatter, render_points_as_spheres=True,
                      point_size=10 ,scalars=dataset_scatter[:, 0])

# We add the label objects to the plotter object, set the point size, the font size and set them to be always visible - no culling
pl.add_point_labels(label_points, label_names, point_size=5, font_size=26, always_visible=True)

# We setup the 3D grid, hide the month labels on the grid and rename the axis labels
pl.show_grid(show_zlabels= False, xlabel = "Temperature", ylabel="Humidity", zlabel="Months", location="origin")
# Setup a callback function that rotates the camera around the scene
pl.add_callback(update_scene, interval=100)

# Show the plotter
pl.show()
pl.app.exec_()




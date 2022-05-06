import vedo
from vedo.pyplot import histogram
import numpy as np
import pandas as pd
import os
'''
Pandas data pre-processing
'''
# Load the csv data
dataset_path = os.path.join('dataset','metadata.csv')
dataset = pd.read_csv(dataset_path)  
print(dataset.head())

# Transform the DateTime column to pandas datetime
dataset['DateTime']=  pd.to_datetime(dataset['DateTime'], format='%d/%m/%Y %H:%M')
# Create a months column and multiply it by an arbitrary separation value for easier visualization
separation_factor = 10
dataset['Months'] = dataset['DateTime'].dt.month * separation_factor
# Create a column with the month names for visualization in each window
dataset['Months_name'] = dataset['DateTime'].dt.month_name()
dataset_scatter = dataset[['Temperature', 'Humidity','Months']].to_numpy()

# Get unique months and unique month names
unique_months = dataset['Months'].unique()
unique_months_name = dataset['Months_name'].unique()


'''
Vedo dataset visualization
'''
# Initialize a vedo plotter, with N number of subfigures, axis shown at each one and each window has separete camera
plt = vedo.Plotter(N=len(unique_months)+2, axes=1, sharecam = 0, size=(2100, 1150))

# Initialize 3D point cloud from the dataset columns and visualize on the first subfigure
pc = vedo.Points(dataset_scatter, r=5)
pc.cmap("Blues_r", dataset_scatter[:,2]) # colorize points by their value in z
# Show a label that always faces camera
vig = pc.vignette("August", font="Quikhand", point=(20,60,80), c='white').followCamera()
plt.at(0).show(pc, vig, bg='black',axes=1)

# For each month generate separate points and a separate subfigure
for idx, month in enumerate(unique_months):
    # Get all rows from a specified month
    curr_points = dataset_scatter[dataset_scatter[:,2]== month,:]
    # change the 3rd dimension to 1s so we can more easily show each of the months
    curr_points[:,2] = np.ones_like(curr_points[:,2])
    # Generate the points of that month with 50% alpha so we can also visualize a density heatmap on top
    pc_temp = vedo.Points(curr_points, r=8, c="blue5", alpha=0.5)
    # Create a density heatmap as a volume
    vol = pc_temp.density().c('Dark2').alpha([0.1,1]) 
    # the relative automatic radius used for calculating the density for each plot
    r = vedo.precision(vol.info['radius'], 2) # retrieve automatic radius value
    # Add a scalar bar with the calculated density radius
    vol.addScalarBar3D(title=f'Month {unique_months_name[idx]} density (counts in r_s ={r})', c='k', italic=1)
    # Plot the month on a separate subfigure together with the density plot
    plt.at(idx+1).show(pc_temp, vol, __doc__, axes=1)

# Generate the histogram as a temperature/humidity of the dataset
histo = histogram(
    dataset["Temperature"], dataset["Humidity"],
    bins=10,
    mode='hexbin',
    xtitle="Temperature",
    ytitle="Humidity",
    ztitle="counts",
    fill=True,
    cmap='terrain',
)
# Plot the histogram at the subfigure.
plt.at(len(unique_months)+1).show(histo, axes=1, viewup='z')
# Initialize the plotter and visualize
plt.interactive().close()
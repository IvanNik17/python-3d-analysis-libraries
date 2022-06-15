import pyvista as pv
from pyvistaqt import BackgroundPlotter
import os
import numpy as np

# Class on building a replica point cloud one point neighbourhood at a time. 
class find_neighbours():
    def __init__(self,pc_points, num_neighbours):
        # Setup initial variables - get the point cloud, set a counter for the current point selected, getting the neighborhood
        # setup a array of booleans to keep track of the points that have been already checked and setting up the plotter
        self.pc_points = pc_points
        self.counter = 0
        self.num_neighbours = num_neighbours
        self.checked = np.zeros(len(pc_points), dtype=bool)
        self.p = BackgroundPlotter()


    # Update function called by the callback
    def every_point_neighborhood(self):
        # get the current point to calculate the neighborhood of
        point = pc_points[self.counter,:]
        # get all the indices of the neighbors of the current point
        index = pc.find_closest_point(point,self.num_neighbours)
        # get the neighbor points
        neighbours = pc_points[index,:]
        # mark the points as checked and extract the checked sub-point cloud
        self.checked[index] = True

        new_pc = pc_points[self.checked]
        # move the reconstructed point cloud in X direction so it can be more easier seen
        new_pc[:,0]+=1
        # add the neighborhood points, the center point and the new checked point clouds to the plotter.
        # Because we are using the same names PyVista knows to update the already existing ones
        self.p.add_mesh(neighbours, color="r", name='neighbors', point_size=8.0, render_points_as_spheres=True)
        self.p.add_mesh(point, color="b", name='center', point_size=10.0, render_points_as_spheres=True)
        self.p.add_mesh(new_pc, color="g", name='new_pc', render_points_as_spheres=True)
        # move the counter with a 100 points so the visualization is faster - change this to 1 to get all points
        self.counter+=100
        # get the point count
        pc_count = len(pc_points)
        # check if all points have been done. If yes then 0 the counter and the checked array
        if self.counter >= pc_count:
            self.counter = 0
            self.checked = np.zeros(len(pc_points), dtype=bool)

        # We update the whole plotter
        self.p.update()
    # visualization function
    def visualize_neighbours(self):
        # add the colored mesh of the duck statue. We set the RGB color scalar array as color by calling rgb=True
        self.p.add_mesh(pc, render_points_as_spheres=True, rgb=True)
        # We set the callback function and an interval of 100 between update cycles
        self.p.add_callback(self.every_point_neighborhood, interval=100)
        self.p.show()
        self.p.app.exec_()



# Class of parameters used in the two callback function
class params():
    # size of the neighborhood 
    size = 20
    # the selected point
    point = np.zeros([1,3])
    # is the point selected or not
    point_selected = False

# Callback function for selecting points with the mouse
def manipulate_picked(point):
    # Get selected point and switch the boolean for having selected something to True
    params.point = point
    params.point_selected = True
    # Get the closest points indices 
    index = pc.find_closest_point(point,params.size)
    # Get the points themselves
    neighbours = pc_points[index,:]
    # add points representing the neighborhood and the selected point to the plotter
    p.add_mesh(neighbours, color="r", name='neighbors', point_size=8.0, render_points_as_spheres=True)
    p.add_mesh(point, color="b", name='center', point_size=10.0, render_points_as_spheres=True)

# Callback function for the slider widget for changing the neighborhood size 
def change_neighborhood(value):
    # change the slider value to int
    params.size = int(value)
    # call the point selection function if a point has already been selected
    if params.point_selected:
        manipulate_picked(params.point)

    return


def connectivity_filter(pc):
    # Use the connectivity filter to get the scalar array of region ids
    conn = pc.connectivity(largest=False)
    # See the active scalar fields in the calculated object
    print(conn.active_scalars_name)
    # Show the ids
    print(conn["RegionId"])
    # Set up a plotter
    p = pv.Plotter()
    # add the interactive thresholding tool and show everything
    p.add_mesh_threshold(conn,show_edges=True)
    p.show()
    

if __name__ == '__main__':

    # Read the duck statue point cloud
    pc_path = os.path.join('point_cloud','duckStatue.ply')
    pc = pv.read(pc_path) 

    pc_points = pc.points
    pc_points = np.array(pc_points)


    ## Part 1 Initialize class for reconstructing of the point cloud one neighborhood at a time
    # neighbours_class = find_neighbours(pc_points, 400)
    # neighbours_class.visualize_neighbours()

    ## Part 2 Manual selection of points and calculating neighborhoods based on a slider size
    # Initialize the plotter
    p = pv.Plotter()
    # Add the main duck statue point cloud as spheres and with colors 
    p.add_mesh(pc, render_points_as_spheres=True, rgb=True)
    # Initialize the mouse point picker callback and the slider widget callback
    p.enable_point_picking(callback=manipulate_picked,show_message="Press left mouse to pick", left_clicking=True)
    p.add_slider_widget(change_neighborhood, [10, 300], 20, title='Neighbourhood size', event_type = "always")
    p.show()



    ## Part 3 Connectivity filter function
    # connectivity_filter(pc)

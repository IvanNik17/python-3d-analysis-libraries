import numpy as np
import polyscope as ps
import time
import os

# Callback function called every update iteration.  The same functions can be used for GUI functionality and interactivity
def callback():
    # get the delta time
    delta_change = time.time()
    # create a 4x4 matrix for the angel statue rotation
    matrix=np.eye(4)
    # create a rotation in Y direction using the delta_change
    rotation = np.array([[np.cos(delta_change), 0, np.sin(delta_change)], [0, 1, 0], [-np.sin(delta_change), 0, np.cos(delta_change)]])
    # multiply the rotation with the points of the point cloud
    new_points = np.dot(points,rotation.T)
    # updathe the point positions in the renderer
    ps_cloud.update_point_positions(new_points)

    # compute the X and Z position of the sphere point 
    xpos = np.sin(-delta_change*2)
    zpos = np.cos(-delta_change*2)
    # Update the point position with the new X and Z positions.
    ps_sphere.update_point_positions(np.array([[xpos,1,zpos]]))


# Load the angel point cloud
pc_path = os.path.join('point_cloud','angelStatue_lp.txt')
point_cloud = np.loadtxt(pc_path, delimiter=' ')
# Separate the point array into point positions and colors. The colors need to be between 0-1, so we cast the ints to floats and divide by 255
points = point_cloud[:,:3]
colors = point_cloud[:,3:6].astype(np.float32)/255


# Initialize the polyscope environment. Calling this is required before the show method can be invoked
ps.init()
# Initialize a polyscope point cloud with a specific name, point positions and material. We need a material that supports blending so the colors can be visualized - 'clay', 'wax', 'candy', 'flat'
ps_cloud = ps.register_point_cloud("angel", points, enabled=True, material = 'clay')
# Add the color information to the point cloud and enable it
ps_cloud.add_color_quantity("angel colors", colors, enabled = True)

# create a point cloud of one point for the 'sphere' that rotates around the angel statue
point = np.array([[1,1,1]])
# Initialize the "sphere" point and render it as a sphere. We give it an interesting material that does not need to be blended
ps_sphere = ps.register_point_cloud("point", point, point_render_mode='sphere', material='ceramic')
# Set the radius of the sphere
ps_sphere.set_radius(0.1, relative=False)

# Set the callback function for the animation
ps.set_user_callback(callback)
# Show the scene
ps.show()
# Clean up the callbacks
ps.clear_user_callback()

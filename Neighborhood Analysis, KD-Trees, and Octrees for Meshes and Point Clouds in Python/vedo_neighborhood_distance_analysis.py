import vedo
import os

# Simple helper class containing a list containing the two points between which we calculate the geodesic distance
# And the currently selected point
class params():
    points_list =[]
    point = []

# Callback function for calculating the geodesic distance between two selected points
def calculate_geodesic(evt):
    # Check if the click has selected a object
    if evt['actor'] != None:
        # Get the 3D point from the selected object
        params.points_list.append(evt['picked3d'])
        # if there are more than 2 points in the point list remove the first one
        if len(params.points_list) > 2:
            params.points_list.pop(0)
        # if there are exactly 2 points calculate the geodesic distance between them and visualize the path
        if len(params.points_list) == 2:
            # get point 1 and point 2 from the list
            point_1 = params.points_list[0]
            point_2 = params.points_list[1]

            print(point_1, point_2)
            # Calculate the geodesic distance and get the path in red color
            path = mesh.geodesic(point_1, point_2).c("red4")
            # Make two point clouds representing the first and second points in different colors 
            p1 = vedo.Points([point_1], r=20).color("blue")
            p2 = vedo.Points([point_2], r=20).color("green")
            # if there are more than 4 objects remove the old 3 ones
            if len(plt.actors)==4:
                for i in range(0,3): plt.pop()
            # add the new ones
            plt.add(path, p1, p2)

        # render
        plt.render()

# Callback function for selecting a point, calculating its neighborhood, calculating the average normal and fitting a circle to the neighborhood
def fit_circle(evt):
    # Check if anything has been clicked on
    if evt['actor'] != None:
        # From the event get the 3D point that has been selected
        params.point = evt['picked3d']

        # Find all the indices of points in a radius around the clicked point
        closets_ids = mesh.closestPoint(params.point, radius = 0.01, returnPointId = True)
        all_points = mesh.points()
        # get the neighbor points
        closets_points = all_points[closets_ids,:]
        # get their normals
        closets_normals = mesh.normals()
        closets_normals = closets_normals[closets_ids,:]
        # Calculate the average normal of the neighborhood
        closets_normals_avg = closets_normals.mean(axis=0)
    
        # Make the selected point and its neighborhood into Vedo point clouds
        center_point = vedo.Points([params.point], r=20).color("red")
        neighbourhood = vedo.Points(closets_points, r=10).color("blue")
        # Fit a circle to the neighborhood points and return the circle center, radius and normal or orientation
        (center_circle, radius, normal_to_circle) = vedo.fitCircle(closets_points)
        # Create a circle 3D object, make into a wireframe and orient it based on the circle normal
        circle = vedo.Circle(center_circle, r=radius).wireframe().orientation(normal_to_circle)
        # Create a end point for the array object showing the average normal - 0.05 is a scaling factor
        end_point = params.point + closets_normals_avg*0.05
        # Make an arrow object
        arrow = vedo.Arrow(startPoint=params.point, endPoint=end_point, c='red')
        # Check if t he created objects in the Plotter are equil to 5, if they are remove them
        if len(plt.actors)==5:
            for i in range(0,4): plt.pop()
        # add the new created objects
        plt.add(center_point, neighbourhood, circle, arrow)


if __name__ == '__main__':

    # Load the bunny mesh Ply file
    mesh_path = os.path.join('mesh','bun_zipper.ply')
    mesh = vedo.load(mesh_path)

    # Set the interactivity of the Plotter to true
    vedo.settings.allowInteraction = True
    # Create a plotter object with a black background
    plt = vedo.Plotter(bg = 'black', interactive = False)

    # Part 1 calculate geodesics 
    # Create set a function to the timer callback
    plt.addCallback('LeftButtonPress', calculate_geodesic)

    ## Part 2 calculate the fit circle
    # plt.addCallback('LeftButtonPress', fit_circle)

    # Show the bunny mesh, change the background to black, view up direction to Z and zoom level
    plt.show(mesh, __doc__, bg2='black', viewup="z", zoom=1.3)

    # Set again the plotter to interactive and stop everythin after it has been closed.
    plt.interactive().close()


import vedo
import os


# Paths to the angel mesh and texture
mesh_path = os.path.join('mesh','angelStatue_lp.obj')
texture_path = os.path.join('mesh','angelStatue_lp.jpg')

# Load the mesh, add the texture to the mesh and set up a material for the mesh.
# A bit confusing but the material properties are invoked with .lighting
mesh = vedo.load(mesh_path).texture(texture_path)
mesh.lighting('default')

# Create a box primitive with specified length, width and height. Move it 1 in Z direction, color it white and make it glossy
floor = vedo.Box(length = 5, width = 5, height = 0.1).z(1).c('white').lighting('glossy')
# Rotate it 90 degrees in the X axis
floor.rotate(90)
# Create a sphere with a radius and position and make it metallic
sphere = vedo.Sphere(r=0.2).pos(1,0,0)
sphere.lighting('metallic')

# Create  two lights one on the position of the sphere with an intensity of 2 and blue color and one above and to the right of the angel with a lower intensity and white color
l1 = vedo.Light(sphere, c ='blue5',intensity = 2) 
l2 = vedo.Light((1,2,1), c ='white',intensity = 1) 

# Set this to true if you want to be able to create interactions and animations for your scene
vedo.settings.allowInteraction = True
# Create a plotter object with a black background
plt = vedo.Plotter(bg = 'black', interactive = False)

# Call this if you want shadows to be visualized in your scene
plt.addShadows()

# Call show with all the 3D objects and lights that you wan to add to the scene
vedo.show(mesh, floor, sphere, l1, l2)

# Option1: create a forever look which we can stop by closing the window
# Create a forever look which we can stop by closing the window
# while True:
#     # Rotate the angel mesh each loop cycle  with a certain amount in Y axis. 
#     mesh.rotateY(2)
#     # Rotate sphere around y axis in opposite direction. You can specify the point around which the object rotates as well
#     sphere.rotateY(-3, around=(0,0,0))
    
#     # Get the position of the sphere
#     sphere_pos = sphere.pos()
#     # Set the light position to the position of the sphere
#     l1.SetPosition(sphere_pos)
#     # Render the whole scene to show all changes
#     plt.render()
#     # check if X button has been pressed to stop the loop
#     if plt.escaped:
#         break

# Option2: Create a callback function
# Function called from the timer callback every delta time
def rotate_objects(evt):
    mesh.rotateY(2)
    # Rotate sphere around y axis in opposite direction. You can specify the point around which the object rotates as well
    sphere.rotateY(-3, around=(0,0,0))
    
    # Get the position of the sphere
    sphere_pos = sphere.pos()
    # Set the light position to the position of the sphere
    l1.SetPosition(sphere_pos)
    # Render the whole scene to show all changes
    plt.render()

# Create a timer event callback with a delta 10
plt.timerCallback("create", dt=10)
# Create set a function to the timer callback
plt.addCallback('timer', rotate_objects)

# Set again the plotter to interactive and stop everythin after it has been closed.
plt.interactive().close()
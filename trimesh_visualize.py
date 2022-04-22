import time
import trimesh
import numpy as np

def rotate_objects(scene):

    # create an empty homogenous transformation
    matrix = np.eye(4)

    delta_change = time.time()
    # set Y as cos of time
    matrix[0][3] = np.sin(-delta_change*2)
    # set Z as sin of time
    matrix[2][3] = np.cos(-delta_change*2)

    # create a y axis rotation
    yaxis = [0,1,0]
    Ry = trimesh.transformations.rotation_matrix(delta_change*2, yaxis)

    node_sphere = s.graph.nodes_geometry[0]
    node_mesh = s.graph.nodes_geometry[1]


    
    # apply the transform to the node
    scene.graph.update(node_sphere, matrix=matrix)
    scene.graph.update(node_mesh, matrix=Ry)

if __name__ == '__main__':
    # create some spheres
    a = trimesh.primitives.Sphere(radius=0.1)


    # set some colors for the balls
    a.visual.face_colors = [0, 0, 255, 255]

    mesh_path = 'mesh/angelStatue_lp.obj'
    mesh = trimesh.load(mesh_path)


    # create a scene with the two balls
    s = trimesh.Scene([a,mesh])

    print(s.graph.nodes)

    # open the scene viewer and move a ball around
    s.show(callback=rotate_objects)
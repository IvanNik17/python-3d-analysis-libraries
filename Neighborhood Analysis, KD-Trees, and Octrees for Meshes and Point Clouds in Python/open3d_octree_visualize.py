import numpy as np
import open3d as o3d
import pandas as pd
import os





point_cloud_path = os.path.join('point_cloud','duckStatue.ply')
point_cloud = o3d.io.read_point_cloud(point_cloud_path)


octree = o3d.geometry.Octree(max_depth=10)
octree.convert_from_point_cloud(point_cloud, size_expand=0.01)
o3d.visualization.draw_geometries([octree])

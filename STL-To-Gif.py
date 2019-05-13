# -*- coding: cp1252 -*-

##############################
#                            #
# Created by: Daniel Aguirre #
# Date: 2019/05/13           #
#                            #
##############################

# Imports
import os, re, math, sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh
import imageio

# USER´s VARIABLES
# General parameters
filename_stl = "T-REX skull.stl"
filename_gif = "T-Rex skull.gif"
path = "frames/"

# GIF´s parameters
frames = 25
duration_frame = 0.1

# Visualization parameters
init_angle = -80
elevation = 8
rotation_axises = [0.0, 1.0, 0.0]
rotation_angle = 90
x_offset = 0
y_offset = 0
z_offset = 0

# Checks that input paratmeters are correct
def initialize():
    global frames
    if (frames<=0):
        frames = 25

# Loads the STL file
def loadSTL():
    global stl_mesh
    stl_mesh = mesh.Mesh.from_file(filename_stl)

def rotateSTL():
    stl_mesh.rotate(rotation_axises, math.radians(rotation_angle))

# Creates frames for the gif
def createFrames():

    # Center the STL
    x_min = stl_mesh.vectors[:,:,0].min()
    x_max = stl_mesh.vectors[:,:,0].max()
    y_min = stl_mesh.vectors[:,:,1].min()
    y_max = stl_mesh.vectors[:,:,1].max()
    z_min = stl_mesh.vectors[:,:,2].min()
    z_max = stl_mesh.vectors[:,:,2].max() 

    x_center_offset = (x_max + x_min)/2.0
    y_center_offset = (y_max + y_min)/2.0
    z_center_offset = (z_max + z_min)/2.0

    stl_mesh.vectors[:,:,0] = stl_mesh.vectors[:,:,0] - x_center_offset - x_offset
    stl_mesh.vectors[:,:,1] = stl_mesh.vectors[:,:,1] - y_center_offset - y_offset
    stl_mesh.vectors[:,:,2] = stl_mesh.vectors[:,:,2] - z_center_offset - z_offset
    
    # Create a new plot
    figure = plt.figure()
    axes = mplot3d.Axes3D(figure)

    # Add STL vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors))
    axes.add_collection3d(mplot3d.art3d.Line3DCollection(stl_mesh.vectors,color="black",linewidth=0.5))
    axes.view_init(elev=35., azim=-45)

    # Auto scale to the mesh size
    scale = stl_mesh.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Deactivate Axes
    plt.axis('off')

    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    for i in range(frames):    
        # Rotate the view
        axes.view_init(elev=elevation, azim=init_angle + 360/frames*i)
    
        # Save frame
        frame_i = "frame_" + str(i)
        print("Saved: " + str(frame_i))
        plt.savefig(path + frame_i + ".png")

# Loads frames and creates gif
def createGif():
    images = []
    files = os.listdir(path)
    ordered_files = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x))
    for file_name in ordered_files:
        if file_name.endswith('.png'):
            file_path = os.path.join(path, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(filename_gif, images, duration = duration_frame)

# MAIN
def main():
    print("Started")
    initialize()
    loadSTL()
    rotateSTL()
    createFrames()
    print("Creating gif")
    createGif()
    print("Finished")
    
main()


    






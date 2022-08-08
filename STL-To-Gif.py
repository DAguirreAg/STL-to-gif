# -*- coding: cp1252 -*-

##############################
#                            #
# Created by: Daniel Aguirre #
# Date: 2019/05/13           #
#                            #
##############################

# Imports
import os, re, math, sys
import sys, getopt, shutil
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from stl import mesh
import imageio

# USERs VARIABLES
# General parameters
inputfile         = None
outputfile        = None

# GIFs parameters
frames            = 25
duration_frame    = 0.1

# Visualization parameters
init_angle        = 0
elevation         = 0
rotation_axises   = [1.0, 0.0, 0.0]
rotation_angle    = 0
x_offset          = 0
y_offset          = 0
z_offset          = 0
render_color      = "blue"
render_line_color = "black"
render_line_width = 0.01
render_width      = 8
render_height     = 6
mov_flag          = False
mov_fps           = 30

path = os.path.join(os.getcwd(), "frames")
for f in os.listdir(path):
    os.remove(os.path.join(path, f))

# Checks that input paratmeters are correct
def initialize():
    global frames, duration_frame, outputfile

    if (frames<=0):
        print("Setting default of frames to 25")
        frames = 25

    if (duration_frame<=0):
        print("Setting default duration to 0.1")
        duration_frame = 0.1

    if inputfile == None:
        print("Error: Inputfile not specified")
        sys.exit(2)

    if outputfile == None:
        outputfile = "output.gif"

# Loads the STL file
def loadSTL():
    global stl_mesh
    stl_mesh = mesh.Mesh.from_file(inputfile)

# Rotate the STL
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
    figure = plt.figure(figsize=(render_width, render_height), dpi=72)
    axes = mplot3d.Axes3D(figure)

    # Add STL vectors to the plot
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors,color=render_color))
    axes.add_collection3d(mplot3d.art3d.Line3DCollection(stl_mesh.vectors,color=render_line_color,linewidth=render_line_width, antialiased=True))
    axes.view_init(elev=35., azim=-45)

    # Auto scale to the mesh size
    scale = stl_mesh.points.flatten()#-1)
    axes.auto_scale_xyz(scale, scale, scale) # divide this to make it bigger, but bounded by window size

    # Deactivate Axes
    plt.axis('off')

    # Delete folder containing frames from previous runs
    if os.path.exists(path):
        shutil.rmtree(path)

    # Create a folder to contain the frames
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    print(f'init_angle: {init_angle}')
    for i in range(frames):
        # Rotate the view

        axes.view_init(elev=elevation, azim=init_angle + 360/frames*i)

        # Save frame
        frame_i = "frame_" + '{0:05d}'.format(i) + ".png"
        print("Saved frames: " + str(i+1) + "/" + str(frames))
        plt.savefig(os.path.join(path, frame_i))

# Loads frames and creates gif
def createGif():
    images = []
    files = os.listdir(path)
    ordered_files = sorted(files, key=lambda x: (int(re.sub('\D','',x)),x))
    for file_name in ordered_files:
        if file_name.endswith('.png'):
            file_path = os.path.join(path, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(outputfile, images, duration = duration_frame)

def createMov():
    # ffmpeg -framerate 30 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p out.mp4
    from subprocess import run
    #duration here
    # run( [ 'ffmpeg', '-framerate 30', '-pattern_type', 'glob', '-i', "%s/*.png"%(path), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'out.mov' ] )
    cmd = 'ffmpeg -y -framerate %s -pattern_type glob -i %s/*.png -c:v libx264 -pix_fmt yuv420p out.mov'%(mov_fps,path)
    run(cmd.split(" "))

# Separate the string into a list of floats
def getList(strlist,separator=","):

    try:
        valueList = list(map(float,strlist.split(separator)))

    except:
        print("Error: Input the values only separated by a comma (,) . I.e: 1,0,0")
        sys.exit(2)

    return list(map(float,strlist.split(separator)))


# MAIN
def main(argv):

    # Main variables
    global inputfile, outputfile, path

    # GIFs parameters
    global frames, duration_frame

    # Visualization parameters
    global init_angle, elevation, rotation_axises, rotation_angle, x_offset, y_offset, z_offset

    # Fork Params
    global render_color, render_line_color, render_line_width, render_width, render_height, mov_flag,mov_fps

    try:
         opts, args = getopt.getopt(argv,"hi:o:p:n:t:a:e:d:r:c:",["help","ifile=","ofile=","nframes=", "duration=", "initangle=", "elevation=", \
         "rotation_angle=", "rotation_axis=", "offset=","path=","color=","linecolor=","linewidth=","outwidth=", "outheight=", "format=","fps="])
    except getopt.GetoptError as e:
         print('Error in args')
         print(e);
         sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage: GCode_to_Robtargets [-h | -i <inputfile> -o <outputfile>] ")
            print('Options and arguments:')
            print("-h     : Print this help message and exit")

            print("-i arg : Input the file to be get the frames for the gif (also --ifile)")
            print("-o arg : Output filename of the gif (also --ofile)")
            print("-p arg : Folder in where the frames will be saved (also --path). If it doesn't exist, it will be created automatically (Default folder: frames)")

            print("-n arg : Amount of frames to generate (also --nframes). Default: 25")
            print("-t arg : Duration (in seconds) of display of each frame (also --duration). Default: 0.1")

            print("-a arg : Starting angle of the first frame (also --initangle). Default: 0")
            print("-e arg : Elevation of the STL (also --elevation). Default: 0")

            print("-d arg : Degrees to rotate the stl (also --rotation_angle). Default: 0")
            print("-r arg : Specify the rotation axis of the STL (also --rotation_axis). Default: [1,0,0]")

            print("--offset arg : Displaces the center from which the STL will revolve. Default: [0,0,0]")

            print("Fork specific options")
            print("--color arg : matplot lib named color or string hexvalue, etc (#ff0000)")
            print("--linecolor : wireframe line colour (black)")
            print("--linewidth : wireframe line width (0.01)")
            print("--outwidth  : width of output inches? (8)")
            print("--outheight : height of output inches? (6)")
            print("--format    : set to mov to create a mov with ffmpeg ()" )
            print("--fps       : only valid for mov, fps (30)")

            sys.exit()

        elif opt in ("-i", "--ifile"):
            inputfile = arg
            print(inputfile)

        elif opt in ("-o", "--ofile"):
            outputfile = arg + ".gif"

        elif opt in ("-p", "--path"):
            path = arg
            path = os.path.join(os.getcwd(), path)

        elif opt in ("-n", "--nframes"):
            frames = int(arg)

        elif opt in ("-t", "--duration"):
            duration_frame = float(arg)

        elif opt in ("-a", "--initangle"):
            init_angle = float(arg)

        elif opt in ("-e", "--elevation"):
            elevation = float(arg)

        elif opt in ("-d", "--rotation_angle"):
            rotation_angle = float(arg)

        elif opt in ("-r", "--rotation_axis"):
            rotation_axises = getList(arg)

        elif opt in ("--offset"):
            offsets = getList(arg)

            x_offset = offsets[0]
            y_offset = offsets[1]
            z_offset = offsets[2]

        elif opt in ("-c", "--color"):
            render_color = arg
            # print("Color is %s"%(render_color))

        elif opt in ("--linecolor"):
            render_line_color = arg
            # print("LColor is %s"%(render_line_color))

        elif opt in ("--linewidth"):
            render_line_width = float(arg)
            # print("LWidth is %s"%(render_line_width))

        elif opt in ("--outwidth"):
            render_width = int(arg)

        elif opt in ("--outheight"):
            render_height = int(arg)

        elif opt in ("--format"):
            if (arg=="mov"):
                mov_flag=True
            else :
                mov_flag=False

        elif opt in ("--fps"):
            mov_fps = float(arg)

    initialize()

    print("Loading STL")
    loadSTL()
    rotateSTL()

    print("Creating frames")
    createFrames()

    if mov_flag:
        print("Calling ffmpeg")
        createMov()
    else:
        print("Creating gif")
        createGif()

    print("Finished")

if __name__ == "__main__":
    print("Started")
    main(sys.argv[1:])

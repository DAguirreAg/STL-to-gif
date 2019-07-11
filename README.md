# STL-to-Gif

This repository contains a Python script to create a gif file from a STL file. The script will automatically center the STL for a better visualization.

<p align="middle">
  <img src="/Examples/T_Rex_skull.png" alt="Input stl file" width="200">

  <img src="/Examples/T_Rex_skull.gif" alt="Output gif file" width="200">
</p>

## How to use
#### Basics
Open a terminal and run the python script passing the STL filename with the `-i` option as follow:

    python STL-To-Gif.py -i inputfile
    python STL-To-Gif.py -i inputfile -o outputfile

#### Modifying the gif
For those of you interested in changing the gif's properties, you have available the following options:

* `--nframes`: Amount of frames that the gif will use.
* `--duration`: Duration of display of each frame.
* `--path`: Folder in where the frames will be saved.

<p align="middle">
  <img src="/Resources/pikachu_dur_0.1.gif" alt="Gif with default frame duration" width="200">
  <img src="/Resources/pikachu_dur_0.2.gif" alt="Gif with frame duration of 0.2s" width="200">
</p>


#### Advanced
Sometimes the STL's position, angle, rotation axis,... are not the most desired ones for creating an appealing gif. For those cases, you have available the following options:

##### Rotating the STL model
For those cases in which the STL model's original orientation is not the most desired one, the following options are available to change the orientation:

* `--rotation_angle`: Degrees to rotate the STL model.
* `--rotation_axis`: Specify the rotation axis of the STL. 

In below example the STL model was rotated 45° around the X axis.

<p align="middle">
  <img src="/Resources/charmander_rot0.gif" alt="Gif with default rotation" width="200" >
  <img src="/Resources/charmander_rot45_in_x.gif" alt="Gif with rotation of 45° around X axis" width="200">
</p>


##### Changing the point of view
Once the model is rotated as desired, sometimes we want to change the camera's point of view as the model will always rotate around the Z axis (looking straight at the image, the up direction). In order to change this, just pass the following option:

* `--elevation`: Elevation of the STL.

In below example the camera's elevation was modified to 20°.

<p align="middle">
  <img src="/Resources/charmander_rot0.gif" alt="Gif with default elevation" width="200">
  <img src="/Resources/charmander_elev_20.gif" alt="Gif with elevation of 20°" width="200">
</p>


##### Other options
* `--initangle`: Starting angle of the first frame. 

<p align="middle">
  <img src="/Resources/bulbasaur_initangle_0.png" alt="Initial frame with default initial angle" width="200">
  <img src="/Resources/bulbasaur_initangle_30.png" alt="Initial frame with initial angle of 30°" width="200">
</p>

* `--offset`: Displaces the center from which the STL will revolve.

<p align="middle">
  <img src="/Resources/squirtle_off_0.gif" alt="Gif with default offset" width="200">
  <img src="/Resources/squirtle_offxy_100.gif" alt="Gif with offset of [100,100,0]" width="200">
</p>

## Future functionalities
In future versions I would like to add a GUI interface for fast checking the resulting gif as well as a faster algorithm to handle big STL files.

## Requirements
You should install the following:

* Python
* Matplotlib
* Numpy
* Numpy-stl
* imageio

## Attributions

The STL files used as an example were not created by me. Find below the corresponding creators:

* T-Rex skull: [Created by 3P3D](https://www.thingiverse.com/thing:330888)
* Pikachu: [Created by FLOWALISTIK](https://www.thingiverse.com/thing:376601)
* Charmander: [Created by FLOWALISTIK](https://www.thingiverse.com/thing:323038)
* Bulbasaur: [Created by FLOWALISTIK](https://www.thingiverse.com/thing:327753)
* Squirtle: [Created by FLOWALISTIK](https://www.thingiverse.com/thing:319413)
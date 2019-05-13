# STL-to-Gif

This repository contains a Python script to create a gif file from a STL file. The script will automatically center the STL for a better visualization.

<p align="middle">
  <img src="/Examples/T-Rex skull.png" alt="Input stl file" width="200">
  <img src="/Examples/T-Rex skull.gif" alt="Output gif file" width="200">
</p>

## How to use
Just open the script and type the stl file you want to convert to a gif in `filename_stl`. You can play around with the `init_angle`, `elevation`, `rotation_axises` and `rotation_angle` for different orientations and rotations.


## Future functionalities
In future versions I would like to add a GUI interface for fast checking as well as a faster algorithm to handle big STL files.

## Requirements
You should install the following:

* Python
* Matplotlib
* Numpy
* stl
* imageio

## For Developers and coders!
I am aware that some parts could be optimized or are redundant for such small program. However I decided to make it as easy and simple as possible for anybody who is new to programming.

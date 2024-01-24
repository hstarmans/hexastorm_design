# Design 
Hexastorm design contains the Computer Animated Design (CAD) files to build an [open hardware fast high resolution laser.](https://reprap.org/wiki/Open_hardware_fast_high_resolution_LASER)  
The CAD file is created out of six PCBs, these can be found in https://github.com/hstarmans/firestarter.  
The design is made using Freecad 0.20 and plugins assembly 4 and Kicad Stepup.  
The main file of interest is assembly_compact.FCStd, in FreeCAD Files.    
Earlier design are available in the branch named old.
The main board is placed in this box 100x67x22mm, AK-NW-84. This box can be found on Aliexpress.

![](./Images/freecadpic.jpg)

## Status
The design is going through a complete redesign.
A summary presentation is available [here](https://youtu.be/b7ArZDhsyfI).

## Instruction Videos
Assembly 4 design, without optical simulation  
https://youtu.be/jhr6iEazbQk  
Assembly 4 design, with optical simulation  
https://youtu.be/kekMkjqzRjE  

## Render 
To create a render of the laser rays, additional code is needed.

FreeCAD workbench  
https://github.com/hstarmans/freecad_hexastorm  
Python library with prism simulation  
https://github.com/hstarmans/opticaldesign  

## Known bugs
 - FreeCAD complains about migration issues, these can be ignored.
 - If the baseplate is changed, screws and local coordinate frames need to be reassigned which is cumbersome

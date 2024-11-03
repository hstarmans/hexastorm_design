# Design 
FreeCAD design for laser direct imager with a prism, for a technical description see [open hardware fast high resolution laser](https://reprap.org/wiki/Open_hardware_fast_high_resolution_LASER).  
The CAD file uses PCBs found here, https://github.com/hstarmans/firestarter.  
Design is made using FreeCAD 1.0.0RC2 with the plugins fasteners and KiCad Stepup.  
The main file of interest is assembly_compact_new.FCStd, in FreeCAD Files.    

<img src="./Images/freecadpic.jpg" align="center" width=70% height=70%>

## Status
Current design will be tested in december 2024 and is intended to be available commercially.

## Instruction Videos
There are some videos on YouTube explaining the design in more details.
These are dated.  
Assembly 4 design, without optical simulation  
https://youtu.be/jhr6iEazbQk  
Assembly 4 design, with optical simulation  
https://youtu.be/kekMkjqzRjE  

## Optical simulation 
Creating the rays in FreeCAD is done using pyoptools and the following two libraries.  
These libraries are hard to use and require extensive time and python knowledge.  
FreeCAD workbench  
https://github.com/hstarmans/freecad_hexastorm  
Python library with prism simulation  
https://github.com/hstarmans/opticaldesign  

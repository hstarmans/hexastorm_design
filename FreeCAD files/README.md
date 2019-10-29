The bill of materials and more details can be found on [Hackaday](https://hackaday.io/project/21933-open-hardware-fast-high-resolution-laser).

If you print all the components, you should be able to build something like shown below;
<img src="https://cdn.hackaday.io/images/7106161566426847098.jpg" align="center" height="300"/>


### Laser height
The laser should be at a height of 29 mm.

### Felix_mount
Used to mount the laser module to the Felix printers frame. 

### Laser tube _support
Should be printed twice, to clamp the laser module.

### Second Cylindrical lens
The second cylindrical lens has a focal length of 25 mm. The lens used is [#48-353](https://www.edmundoptics.com/p/125mm-dia-x-25mm-fl-mgfsub2sub-coated-cylinder-lens/8601/).
The mirror used is 10x10x2 mm, e.g. [#45-517](https://www.edmundoptics.com/p/10-x-10mm-enhanced-aluminum-4-6lambda-mirror/6013/).

### First Cylindrical lens
The first cylindrical lens has a focal length of 75 mm. The lens used is [#48-355](https://www.edmundoptics.com/p/125mm-dia-x-75mm-fl-mgfsub2sub-coated-cylinder-lens/8603/). 

### Laser Housing
The spring selected is [C0180-024-0310M](https://www.asraymond.com/catalog/C01800240310M).
The documentd load length is 4.8 mm and the free length is 7.8 mm and the spring constant is 5 N/mm (32.6lb/in). 

### ATX (power supply)
Mounted to optical plate with 25 mm pitch and M6 holes. Screw used to mount holders to ATX is M3x5.

### Beaglebone fixture
Used to mount Beaglebone to optical plate with 25 mm pitch and M6 holes.

### Optical plate
Thorlabs MB3045/M, aluminum breadboard, 300 mm x 450 mm x 12.7 mm with M6 taps.
4x M6x25 screws to fix scanhead to optical plate
3x M6x12 screws to fix atx to optical plate
2x M6x12 screws to fix beaglebone to optical plate

### Box folder
Used to create the cuts in the box with the FreeCAD LCinterlocking module.

## BOM List
The insert used is Jeveka TAPPEX [M2x3.2](https://www.jeveka.com/nl/catalog/inserts-kato-spirol-ensat-tappex-magneten-magna/tappex-inserts-voor-kunststof/tappex-multisert-inserts-tapxmsm0/tapxmsm00020000/groups/g+c+a+nr+view).
```
M2x3.2       messing insert(4 base, 2 laser, 2 photodiode)          8 pieces 
M2x5         screw laser holder                                     2 units
M2x8         screw holder for PCB                                   2 units
M2           nut                                                    2 units
M2x2         pvc distance bus                                       2 units
M3x22        screw polygon holder                                   4 units (now you use M3x25)
M3           nut                                                    4 units
M3           washer                                                 4 units
```
[C0240-024-0810S](https://www.assocspring.co.uk/round-wire/C0240-024-0810-S) (spring)
```
spring       (2 photodiode, 4 laser unit)                           6 units
M2x6         screw photodiode pcb holder                            3 units
M2           nut                                                    3 units
M2x20        screw photodiode pcb holder in spring                  2 units
M2x8         screw holder second lens                               1 units
M2           washer                                                 1 units
M3x14        screw holds box                                        8 units (now you use M3x16)
M3           nut holds box                                          8 units 
```
## Notes 
#### Spring suppliers
In the Netherlands, one could consider [Alcomex](https://www.alcomex.com) and [Tevema](https://ww.tevema.com).
Use the silicon glue to fix the glasses (CAF3).








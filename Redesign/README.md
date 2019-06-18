# Redesign
The goal of this redesign is to minimize the alignment steps executed by an operator in the fabrication of a laser scanner module.
Via experiment it will be determined if alignment can be reached.

## Design considertions
All constraints are determined with respect to the base plate. The plate is 2 mm thick. The thickness is parallel to the z-axis,
i.e. height.

### Prism Motor
The prism motor is fixed in all dimensions with respect to the base plate.
The offset of the prism motor with respect to the base plate is greater than the protrusion of the prism motor.

### Second Cylindrical lens
The second cylindrical lens has a focal length of 25 mm. The lens used is [#69-774](https://www.edmundoptics.com/p/125mm-h-x-25mm-l-x-25mm-fl-vis-nir-coated-cylinder-lens/24050/).
The second cylindrical lens is placed as close as possible to the prism motor. The second cylindrical lens is parallel to the
edge of the motor base. The line connecting the center of the cylindrical lens with the center of the polygon is orthogonal to edge of the motor base. The height of the base for the second cylindrical lens is such that the center of the lens aligns with the center of the prism motor. The lens is clamped into the holder and screwed into the base so it can be replaced.
The support ridge for the mirror has been set at 1 mm. The edge width has been set at 2 mm; bringing total width to 12.5+2x2=16.5 mm. The height becomes 25+2x2=29 mm.  The fit of the lens has been extended by 300 micrometers for printer inaccuracies, i.e. the edge is 1.7 mm.
The center thickness is 3 mm. The lens can be completely inserted.
Roof is not needed

### Right angle beam manipulator
The beam must be manipulated to reach the photodiode. To ensure all aberations are included, the laser bundle is measured after refracting through the entire prism. The beam can be manipulated by using a prism or a mirror. In the Hexastorm POC of 2019-01, a right-angle prism is used. Due to cost reasons, it was decided to switch to a first surface mirror. The foot of the mirror is integrated with the foot of the second cylindrical lens. The dimensions of the mirror is such that it covers the entire height of the second cylindrical lens. The first surface mirror has dimensions 10x10x2 mm see [source](https://www.edmundoptics.com/p/10-x-10mm-enhanced-aluminum-4-6lambda-mirror/6013/). The mirror will use up to 5 mm of the cylinder lens.

### Photodiode
The photodiode is placed directly after the mirror. The height of the photodiode can be adjusted so the bundle hits the photodiode at its center. The photodiode has a vertical translational degree of freedom of 5 mm. The photodiode is protected by a cap to minimize the influence of stray light. The cap can be removed so the laser can be aligned. The cap will be removable from the top.
The photodiode used is [BPW34B](http://www.farnell.com/datasheets/2711552.pdf).


### First Cylindrical lens
The first cylindrical lens has a focal length of 75 mm. The lens used is [68048](https://www.edmundoptics.com/p/125mm-h-x-25mm-l-x-75mm-fl-mgfsub2sub-coatedcylinder-lens/22744/).The focal length tolerance is 3 percent which is approximately 2 mm. 
The combined focal length tolerance of the two lenses is roughly 3 mm. This is mitaged by giving one translational degree of freedom to the first cylindrical lens. The translational degree of freedom is established along the line connecting the center of the laser and the center of the polygon. As a result, during placement, the lens will also have one rotational degree of freedom with the rotanational axis perpendical to the base plane. This degree of freedom is used to correct for a possible horizontal misalignment of the laser with respect to the prism.
The lens is clamped by a screw. The curved side faces the laser. This is optically better and allows the lens to be supported by a plane with the normal vector against gravity. The inserts used are Jeveka TAPPEX [M2x4](https://www.jeveka.com/nl/catalog/inserts-kato-spirol-ensat-tappex-magneten-magna/tappex-inserts-voor-kunststof/tappex-multisert-inserts-tapxmsm0/tapxmsm00020000/groups/g+c+a+nr+view). The base of the lens is not supported by a cross, as the lens is already clamped from the bottom.
This also allows one not to use the support on the edges of the mirror.
The support ridge for the mirror has been set at 1 mm. The edge width has been set at 2 mm; bringing total width to 12.5+2x2=16.5 mm. The height becomes 25+2x2=29 mm. The offset of the lens from the plane is set at 7.5 mm. The offset in the sketch is therefore 5.5 mm as 2 mm is accounted for by the edge. The fit of the lens has been extended by 300 micrometers for printer inaccuracies, i.e a extra cut of 300 micron all directions has been made. The center thickness is 2 mm. The groove for the lens has been made 2 mm. The whole lens is 4  mm thick. The base and the top have been extended at places where a insert needed to pressed.

### Laser Housing
The laser housing has one vertical degree of freedom. This is needed to ensure the laserdiode hits the center of the prism.
The laser diode housing is kept close to the second cylindrical lens to minimize the footprint. The center of the prism, polygon and laser housing are on a line. The laser is calibrated by four screws which form the basis of the laser housing. Between the housing and the blase plate a stiff spring is placed. Springs can be ordered at Alcomex or Tevema. The height is between 3 (back) and 5 mm (front). 
The spring selected is [C0180-024-0310M](https://www.asraymond.com/round-wire-compression-springs/C01800140750M).
The load length is 7.8 mm and the free length is 19 mm and the spring constant is 0.2 N/m. 

### Base plate size
The distance from the second cylindrical lens to the edge of the base plate should be less than 25 mm. Otherwise, the focal point is reached before the edge of the base plate. The base plate should also have holes for mounting the spindle.

## TODO
- try to reuse / salvage current parts
- order mirror and missing parts
- finalise dimensions parts
- select spring for photodiode

## Notes 
#### Spring suppliers
In the Netherlands, one could consider [Alcomex](https://www.alcomex.com) and [Tevema](https://ww.tevema.com).







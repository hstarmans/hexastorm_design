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
The second cylindrical lens has a focal length of 25 mm.
The second cylindrical lens is placed as close as possible to the prism motor. The second cylindrical lens is parallel to the
edge of the motor base. The line connecting the center of the cylindrical lens with the center of the polygon is orthogonal to edge of the motor base. The height of the base for the second cylindrical lens is such that the center of the lens aligns with the center of the prism motor.

### Right angle beam manipulator
The beam must be manipulated to reach the photodiode. To ensure all aberations are included, the laser bundle is measured after refracting through the entire prism. The beam can be manipulated by using a prism or a mirror. In the Hexastorm POC of 2019-01, a right-angle prism is used. Due to cost reasons, it was decided to switch to a first surface mirror. The foot of the mirror is integrated with the foot of the second cylindrical lens. The dimensions of the mirror is such that it covers the entire height of the second cylindrical lens. The first surface mirror has dimensions 10x10x2 mm. The mirror will use up to 5 mm of the cylinder lens.

### Photodiode
The photodiode is placed directly after the mirror. The height of the photodiode can be adjusted so the bundle hits the photodiode at its center. The photodiode has a vertical translational degree of freedom of 5 mm. The photodiode is protected by a cap to minimize the influence of stray light. The cap can be removed so the laser can be aligned. The cap will be removable from the top.

### First Cylindrical lens
The first cylindrical lens has a focal length of 75 mm. The focal length tolerance is 3 percent which is approximately 2 mm. 
The combined focal length tolerance of the two lenses is roughly 3 mm. This is mitaged by giving one translational degree of freedom to the first cylindrical lens. The translational degree of freedom is established along the line connecting the center of the laser and the center of the polygon. As a result, during placement, the lens will also have one rotational degree of freedom with the rotanational axis perpendical to the base plane. This degree of freedom is used to correct for a possible horizontal misalignment of the laser with respect to the prism.

### Laser Housing
The laser housing has one vertical degree of freedom. This is needed to ensure the laserdiode hits the center of the prism.
The laser diode housing is kept close the second cylindrical lens. The center of the prism, polygon and laser housing are on a line. The laser is calibrated by four screws which form the basis of the laser housing, between the housing and the blase plate 
a stiff spring is placed. Springs can be orderd at Alcomex or Tevema. The height is between 3 (back) and 5 mm (front).

### Base plate size
The distance from the second cylindrical lens to the edge of the base plate should be less than 25 mm. Otherwise, the focal point is reached before the edge of the base plate. The base plate should also have holes for mounting the spindle.

## Approach
Design order; prism motor standoff, laser housing base, first cylindrical lens, second cylindrical lens, right angle beam manipulator
and photodiode holder. Test accordingly.







# Company: Hexastorm
# Author: Henri Starmans
# Date: 14-3-2017

from os import system
from math import sqrt, ceil
from solid.objects import cylinder, cube, polygon, scale, import_stl
from solid.utils import scad_render_to_file, up, mirror, right, linear_extrude
from solid.utils import rotate, left, down, back, forward, hole, translate
from solid.utils import hull

# TODO:
#     * the box is mirrored in the Y plane as the cables on the FELIXprinter are
#     * on the other side
#     * add curved edges --> guilleaume stated this prints better
#     * Logo cannot be rendered via openscad, combine the script with Blender?!
#
# TODO:
# parameters should be shared among functions, i.e. the functions should become
# objects. These objects should have a property like bounding box.

# CONSTANTS
# THICK_WALL
#  The wall thickness is a key parameter for all functions
#  Shapeways advices 2 mm, link https://www.shapeways.com/materials/pla
THICK_WALL = 2  # [mm]

# HEIGHT WALL
#  definess height base box
HEIGHT_WALL = 40  # [mm]

# The top of the box is THICK_WALL thick
# The maximum height for logo placeholders etc.
# is HEIGHT_TOP
HEIGHT_TOP = 7  # [mm]
# box is kept in place by four screws
# TODO: from threaded insert holesize/2 + thick
# screw_fixoffst, actual ofset is actually one wallthick more
#                --> holesize/2 + thick*2
SCREW_FIXOFFST = 8.5  # [mm]
LENGTH_TOP = 170   # [mm]
WIDTH_TOP = 108     # [mm]
# laser height = prism offset, polygon axis, guarantee laserbase renders
LASER_HEIGHT = 12.5 + 7.2 + 5
# lighthole the extent of the light gap, global as its needed by top box,
# mirror mount and bottom box
light_hole = 10  # [mm]

# TIE_WIDTH, TIE_HEIGHT
# fastener for the cable is tie-wrap 150 x 2.5 mm with h = 3 and w = 4 mm
TIE_WIDTH = 4
TIE_HEIGHT = 10


def screw(r_head, h_head, r_shaft, length, thick=THICK_WALL):
    """screw
    create a hole so a screw can be screwd into the box

    the center of the screw is aligned with the center of the coordinate system
    the screw is oriented as flipped T, i.e. it is standing on its head.
    screws are generated with an enclosing of THICK_WALL mm
    the interior is ensured via the hole function
    it is assumed that r_head > r_shaft
    The height of the head is h_head, an additional r_head-r_r_shaft is added
    to ensure printablity.

    :param r_head: radius of the head of the screw [mm]
    :param h_head: height of the head of the screw [mm]
    :param r_shaft: radius of the shaft of the screw [mm]
    :param length: desired length of the screw [mm]
    """
    h_shaft = length - h_head - (r_head - r_shaft)
    head = cylinder(h=h_head, r=r_head, segments=30)
    # 45 degrees cone for printability
    cone = up(h_head)(cylinder(h=r_head-r_shaft, r1=r_head,
                               r2=r_shaft, segments=30))
    shaft = up(h_head + (r_head - r_shaft))(cylinder(h=h_shaft,
                                                     r=r_shaft, segments=30))
    inner = head + cone + shaft
    screw = cylinder(h=length, r=r_head + thick) - hole()(inner)
    return screw


def lasershim(height):
    """lasershim

    This is a shim which can be used to pad. The base of the shim is in the
    XY plane at quadrant 1. One corner is at the origin. The width is parallel
    to the x-axis.
    The shim can be used if the laserbase is not correctly alligned.
    The laser was provided by Odic Force, productid OFL510-1.

    param: height: defines height shim [mm]
    """
    # PARAMETER
    xdisp = 48.5     # [mm], x-displacement screw
    ydisp = 16       # [mm], y-displacement screws
    r_shaft = 2+0.5  # [mm], shaft radius screws
    length = 75      # [mm], x-direction length laser
    width = 30       # [mm], y-direction width laser
    screw_offst = 7  # [mm], screw offset  +x-edge

    # MAXIMAL MATERIAL BASE
    base = cube([length, width, height])
    # screw holes
    screws = cylinder(h=height, r=r_shaft) + right(xdisp)(cylinder(h=height,
                                                                   r=r_shaft))
    spiegel = forward(ydisp / 2)(mirror([0, 1, 0])(back(ydisp / 2)(screws)))
    screws += spiegel
    # create holes
    base -= translate([length - xdisp-screw_offst, (width - ydisp)/2, 0]
                      )(screws)
    return base


def laserbase(laserheight):
    """laserabase
    creates the basis for the laser with ventilation wall

    The laserbase is in the XY plane at quadrant 1.
    One corner is at the origin. The width is parallel to the x-axis.
    The laser was provided by Odic Force, productid OFL510-1.
    The padheight is laser height- 16.5 The laserbundle travels in
    the +x direction and departs from the center, that is 15 mm.
    param: laserheight: the desired height of the laser
    """
    # The laser tube is at 8 mm from bottom.
    # The laser tube has a diameter of 17 mm
    # The laser is at 8 + 17 * 0.5 - 1  = 16.5 mm (shim of 1 mm needed)
    # The laser base is 30x60 mm, which was made
    # 30x75 mm to make room for the ventilator

    # PARAMETERS
    height = laserheight-15.5    # [mm],
    xdisp = 48.5                 # [mm], x-displacement screws
    ydisp = 16                   # [mm], y-displacement screws
    r_shaft = 2                  # [mm], shaft radius screws
    h_head = 5                   # [mm], height shaft head
    r_head = 3.5                 # [mm], top radius screws
    tspile = 4                   # [mm], y-thickness ventilation spile
    hspile = 25                  # [mm], height ventilation spile
    length = 75                  # [mm], x-direction length laser
    width = 30                   # [mm], y-direction width laser
    screw_offst = 7              # [mm], screw offset +x-edge

    # MINIMAL MATERIAL BASE
    screws = screw(r_head, h_head, r_shaft, height) + right(xdisp)(
        screw(r_head, h_head, r_shaft, height))
    spiegel = forward(ydisp/2)(mirror([0, 1, 0])(back(ydisp/2)(screws)))
    screws += spiegel
    base = translate([length-xdisp-screw_offst, (width-ydisp)/2, 0])(
        screws)
    # ventilation wall
    # spile
    spile = up(height)(cube([THICK_WALL, tspile, hspile]))
    nofspiles = ceil((width)/(tspile*2))
    # shift base
    base = right(THICK_WALL)(base)
    # add wall
    base += cube([THICK_WALL, width, HEIGHT_WALL])
    # create pockets
    for i in range(0, nofspiles):
        base -= hole()(forward(i*2*tspile + THICK_WALL)(spile))

    return base


def polygonshim(height):
    """polygonshim

    The polygon shim is located in first quadrant of the XY plane.
    A corner is at the origin. The width is parallel to the y-axis.
    The shim can be used to align the polygon.
    The shim was designed for polygon mirror Motor aficio 1018 G029-196.

    :param height: height shim
    """
    # BASE:
    length = 68      # mm [y-direction]
    width = 48       # mm [x-direction]
    r_shaft = 2      # mm shaft radius
    slot_width = 2   # width slot
    base = cube([width/2, length, height])

    def slot(radius, height, width):
        """slot

        openscad styled vertically oriented printable slot
        origin formed by the center of the left circle

        :param radius: the radius of the top of the screw
        :param height: the height of the slot
        :param width: the width of the slot, i.e. distance between radii
        """
        cyl = cylinder(h=height, r=radius)
        outer = hull()(cyl, right(width)(cyl))
        return outer

    # create 2 screw slots
    simple_slot = slot(r_shaft, height, slot_width)
    base -= translate([3.1, length-4, 0])(simple_slot)
    base -= translate([3.2, 4+1.29, 0])(rotate([0, 0, -50])(simple_slot))
    # create hole for polygon rotation axis
    base -= translate([24, 24, 0])(cylinder(h=height, r=10))
    # create hole for polygon lock
    base -= translate([24-7.5, 0, 0])(cube([15, 10, height]))
    #  mirror and add to original
    spiegelold = right(width)(mirror([1, 0, 0])(base))
    base += spiegelold
    return base


def polygonbase(laserheight):
    """polygonbase

    defines the base of a polygon

    The polygon base is located in the first quadrant of the XY plane.
    A corner is at the origin. The width is parallel the y-axis.
    The laser bundle is at 24 mm in the y-direction and the laser bundle
    should be between [10.65, 13.65] mm in the z-direction.
    The height of the base is laserheight - 12.15 mm.
    The height of the base should be at least 7.2 mm. The polygon motor result
    in a protrusion.
    The laser is directed in the +x-direction. The length is oriented along
    y-axis, 21000 RPM polygon
    base could be rotated if laserbase is made smaller. New polygon base at
    24000 RPM seems to be harder to rotate.
    The polygon rotates clockwise.

    :param laserheight: the desired height of the laser, [mm]
    """
    # TODO: the polygon is larger than its, it has a negative x- and y-extent
    # BASE:
    length = 68                  # [mm], y-direction
    width = 48                   # [mm], x-direction
    height = laserheight - 12.5  # [mm]
    r_shaft = 2                  # [mm], shaft radius
    r_head = 3.5                 # [mm], head radius
    h_head = 5                   # [mm], head insert
    slot_width = 2               # [mm], width slot

    def slot(r_head, h_head, r_shaft, width, height):
        """slot

        openscad styled vertically oriented printable slot
        origin formed by the center of left circle

        :param r_head: the radius of the top of the screw, [mm]
        :param h_head: the height of the top of the screw, [mm]
        :param r_shaft: the radius of the shaft of the  screw, [mm]
        :param width: the width of the slot, [mm]
        :param height: the height of the slot, [mm]
         """
        h_shaft = height - h_head - (r_head - r_shaft)
        head = cylinder(h=h_head, r=r_head, segments=30)
        # 45 degrees cone for printability
        cone = up(h_head)(cylinder(h=r_head-r_shaft, r1=r_head, r2=r_shaft,
                                   segments=30))
        shaft = up(h_head + (r_head - r_shaft))(cylinder(h=h_shaft, r=r_shaft,
                                                         segments=30))
        cyl = head + cone + shaft
        inner = hull()(cyl, right(width)(cyl))
        cyl = cylinder(h=height, r=r_head + THICK_WALL)
        outer = hull()(cyl, right(width)(cyl))
        slot = outer - hole()(inner)
        return slot

    wall_slot = slot(r_head, h_head, r_shaft, slot_width, height)
    base = translate([3.1, length-4, 0])(wall_slot)
    base += translate([3.2, 4+1.29, 0])(rotate([0, 0, -50])(wall_slot))
    spiegel = right(width)(mirror([1, 0, 0])(base))
    base += spiegel
    return base


def mirrormount(down, laserheight):
    """mirrormount

    A 25 mm x 25 mm square and 2 mm thick first sided mirror is used to refract
    the ray downward or upward. The thickness is in the +x-direction.
    This mirror is tilted at a 45 degrees and is positioned by a holder.
    The holder is put in place via two pillars.
    A photodiode mount is placed into these pillars to detect the laser motion.
    It is important that the photodiode is at the correct height
    The photodiode_height is LASER_HEIGHT-2.5, to ensure the laser hits the
    photodiode at its center.
    :param down: if true downward refraction, if false upward refraction
    :param laserheight: height laser bundle, [mm]
    """
    width_mirror = 25                     # [mm]
    # thickness y+ pillar, y- pillar is insert+THICK_wall
    tpillar_left = 14                     # [mm]
    insert_mirror = 5                     # [mm]
    thick_mirror = 2                      # [mm]
    # height_mirror < photodiode_height
    height_mirror = laserheight-6       # [mm]
    # 4.5 determined via felix printed box
    photodiode_height = laserheight-4.5  # [mm]
    cable_guide = 2                       # [mm]
    # sensor width with cables is 5.6 (measurement @diode)
    sensor_width = 2                      # [mm]
    # sensor height is 4 (measurement @ photodiode)
    sensor_height = 4.5                   # [mm]
    sensor_insert = 2                     # [mm] diode thickness i 2 @ measured
    # margin is needed for FFF printer
    margin = 0.5                          # [mm]
    # defines the thickness of the holder
    thick = 1.3                           # [mm]
    # offset constraint set by upward proj. due to cable collision possibility
    offset = 19                           # [mm] offset sensor pole
    x_width = 0.5*sqrt(2)*(thick_mirror+margin+2*thick)
    # TODO: xbound seems to be an y_bound
    x_bound = 0.5*sqrt(2)*(2*thick+width_mirror+margin)+x_width
    y_bound = offset+THICK_WALL+sensor_insert

    holder = cube([thick_mirror+margin+2*thick, light_hole+THICK_WALL
                   + insert_mirror+tpillar_left, width_mirror+margin+2*thick])

    holder_inner = translate([thick, 0, thick])(
        cube([thick_mirror+margin, light_hole+tpillar_left+insert_mirror,
              width_mirror+margin]))
    # the holder can contain left over of filament.
    # To remove these left over a cleaning hole is needed.
    holder_inner += translate([thick, 0, thick+width_mirror+margin])(cube([
        thick_mirror+margin, tpillar_left-THICK_WALL, thick]))

    holder -= hole()(holder_inner)
    # up mirror
    holder = up(height_mirror)(rotate([0, 45, 0])(holder))
    # pillars
    # light exit has a width of light_hole
    # pillars are next to this exit point and have a width of tpillar_left,
    # and THICK_WALL + insert_mirror
    mount_mirror = cube([x_width, light_hole + tpillar_left + THICK_WALL
                         + insert_mirror, height_mirror])
    mount_mirror += holder
    # create pocket for light 2x is for certainty
    mount_mirror -= forward(tpillar_left)(cube(
        [2*width_mirror, light_hole, 2*width_mirror]))
    if not down:
        mount_mirror = right(x_bound)(mirror([1, 0, 0])(mount_mirror))

    # add mount photodiode
    # the photodiode is at height photodiode_height mm
    # the cable guides are cable_guide mm thick, the pins of the photodiode
    # are sensor width displaced, the photodiode is sensor height tall
    # the photodiode sensor insert is sensor_insert, the wall between light
    # exit and sensor is fixed at 1 mm, kept small to get maximum out of light
    # path. The top has a three time thickness, to create a connection between
    # mirror and pole
    enclosure = cube([THICK_WALL+sensor_insert, cable_guide*2+sensor_width +
                      THICK_WALL+1, sensor_height +
                      photodiode_height+2*THICK_WALL])
    photodiode = cube([sensor_insert+THICK_WALL, cable_guide*2+sensor_width,
                       sensor_height])
    # substract central pillar
    photodiode -= translate([0, cable_guide, 0])(
        cube([THICK_WALL, sensor_width, sensor_height]))
    # combine pole with photodiode housing
    pole = enclosure - hole()(translate([0, 1, photodiode_height])
                              (photodiode))

    combined = mount_mirror + translate([offset,
                                         tpillar_left+light_hole, 0])(pole)
    # a trafo is executed to simplify positioning;
    # light should be centered at y=0
    combined = translate([y_bound, tpillar_left+0.5*light_hole, 0])(
        mirror([1, 0, 0])(mirror([0, 1, 0])(combined)))
    # add tie-wrap
    # TODO: remove custom parameters
    fasten = translate([9, tpillar_left+9, 0])(
        cable_fasten(TIE_HEIGHT, TIE_WIDTH, THICK_WALL, True))
    combined += fasten

    return combined


def threadedinsert(flip_x, thick, holesize, length):
    """insert
    heatpress insert

    Heatpress can be inserted from the top. The screw should also be inserted
    from the top. The screw is centered at the origin.
    The wall thickness are specified by;
    http://uk.farnell.com/tr-fastenings-brass-inserts-for-plastics
    The length and hole size should be obtained from the sheet.
    this threaded is supported by a triangle and can be mirrored in the
    x-direction
    :param flip_x: flip insert in, origin shifted back
    :param length: length of the insert
    :param holesize: diameter of the hole
    """
    # NOTE: other options
    # -sliding ; this results in a cable collision
    # -press insert; more recommended for photopolymer parts, less permanent
    # -bolt printed inside; requires print pause, not useful in production
    # -magnet; magnets are dangerous for electronics
    x_extent = holesize + 2 * thick
    y_extent = holesize/2 + thick + SCREW_FIXOFFST
    base = cube([x_extent, y_extent, length])
    triangle = polygon([[0, 0], [y_extent, y_extent], [0, y_extent]])
    prism = linear_extrude(x_extent)(triangle)
    support = translate([x_extent, y_extent, 0])(rotate([90, 0, -90])(prism))
    base = support + up(y_extent)(base)
    base -= translate([holesize / 2 + thick, holesize/2 + thick, 0])(
        cylinder(h=length+y_extent, r=holesize/2, segments=30))
    # changed orientation to simplify placement
    base = down(y_extent + length)(base)
    # center origin at Z-axis
    base = translate([-x_extent/2, -SCREW_FIXOFFST+thick+holesize/2, 0])(base)
    if flip_x:
        base = rotate([0, 0, 180])(base)
    return base


def cable_fasten(height, width, thick, x_orient):
    """cable_fasten

    fastener for the cable used is tie wrap 150x2.5 mm with h = 3 and w = 4 mm
    param hoog: height cable fastener
    param width: width cable fastener maximum for FDM is 10 mm
       link http://www.futureengineers.org/Pdfs/startrek/DesignGuidelines.pdf
    param thick: walll thickness
    param x_orient: if true oriented in x-direction otherwise y-direction
    """
    # Altenatives considered:
    # cable fastener: cable clip; (http://www.thingiverse.com/thing:643160)
    #                 might require support and post-processing
    # cable clamp; i.e. two pillars, fixture via friction
    #              might need to be tailored to thickess of cable
    if x_orient:
        base = cube([2*thick+width, thick, height+thick])-right(thick)(
            cube([width, thick, height]))
    else:
        base = cube([thick, 2*thick+width, height+thick])-forward(thick)(
            cube([thick, width, height]))
    return base


def panelmountmini():
    """panelmount

    panel mount for panel Mount cable -B to Mini-B cable
    http://adafru.it/936
    """
    base = cube([40, 20, THICK_WALL], center=True)
    # screw hole
    screw_hole = cylinder(r=1.75, h=THICK_WALL*2, center=True, segments=30)
    # create two holes + hole usb cube
    base -= hole()(left(14)(screw_hole)+right(14)(screw_hole)+cube([
        17.5, 12, THICK_WALL*2], center=True))
    # change orientation
    base = right(0.5*THICK_WALL)(rotate([0, 90, 0])(rotate([0, 0, 90])(base)))
    return base


def createlogo():
    """createlogo

    Openscad cannot handle the Storm font. To mitigate, a vector image of the
    storm font is converted to PNG via Inkscape. The PNG image is linearly
    extruded and converted to a STL.
    This STL is imported by this function, to create the logo.
    """
    # TODO: move Python converter for logo to here
    # LOGO bounding box x  = 234 , y = 26, z = 1
    # scaled to x = 120, y = 13
    x_bound = 120 + THICK_WALL * 2
    y_bound = 13 + THICK_WALL * 2

    # TODO: should throw error !! you removed logo
    logo = scale([0.5, 0.5, 1])(import_stl('hexastorm.stl'))
    logo = None
    # openscad cannot handle minkowski on hexastorm logo
    # logo_mink = up(1)(minkowski()(cylinder(r=0.5, h=1), logo))
    result = translate([-0.5*x_bound, -0.5*y_bound, 0])(
        cube([x_bound, y_bound, 1])) - hole()(mirror([0, 1, 0])(
            logo))
    result = scale([1, 1, HEIGHT_TOP-THICK_WALL])(
        translate([0.5*x_bound, 0.5*y_bound, 0])(result))
    result = up(HEIGHT_TOP-THICK_WALL)(cube([x_bound, y_bound, 1]))
    # TODO: Openscad can create a preview but does not render the logo,
    #      at the moment we resort to
    # modiefs in blender
    return result


def hscrew(head_r, head_height, shaft_r, length):
    """horizontal screw


    a horizontal screw consists out of three parts
    * a cylinder in the wall
    * possible a continuation of the head insert
    * shaft piece
    algorithm ensures it is printable
    param head_height: height head screw
    param head_r: radius head screw
    param shaft_r: radius shaft screw
    param lenght: lenght screw
    """
    # cylinder in the wall
    if head_height > THICK_WALL:
        shift = head_height-THICK_WALL
        cyl_wall = cylinder(h=THICK_WALL, r=head_r+THICK_WALL, segments=30)
        cyl_mid = up(THICK_WALL)(cylinder(h=shift,
                                          r1=head_r+shift+THICK_WALL,
                                          r2=head_r+THICK_WALL, segments=30))
        hscrew = cyl_mid+cyl_wall
    else:
        hscrew = cylinder(h=head_height, r=head_r+THICK_WALL, segments=30)

    # two cases:
    if length-head_height > head_height:
        shift = length-THICK_WALL
        cyl_shaft = up(head_height)(cylinder(h=shift,
                                             r1=shaft_r+shift+THICK_WALL,
                                             r2=shaft_r+THICK_WALL,
                                             segments=30))
    else:
        cyl_shaft = up(head_height)(cylinder(h=length-head_height,
                                             r1=head_r+THICK_WALL,
                                             r2=shaft_r+THICK_WALL,
                                             segments=30))

    hscrew += cyl_shaft
    hscrew = rotate([90, 0, 0])(hscrew)
    # gravity only one direction --> minimize in this direction
    # shaft
    field = cube([2*(shaft_r+THICK_WALL),
                  length-head_height, length+2*shaft_r+THICK_WALL])
    field = translate([-shaft_r-THICK_WALL,
                       -length, -(length+shaft_r)])(field)
    sscrew = hscrew*field
    # top
    if head_height > THICK_WALL:
        field = cube([2*(head_r+THICK_WALL), head_height,
                      length+2*head_r+THICK_WALL])
        field = translate([-head_r-THICK_WALL, -head_height, -(length+head_r)])
        (field)
        tscrew = hscrew*field
    else:
        tscrew = rotate([90, 0, 0])(cylinder(h=head_height,
                                             r=head_r+THICK_WALL, segments=30))

    hscrew = tscrew+sscrew
    cyl_top = down(0.1)(cylinder(h=head_height+0.1, r=head_r, segments=30))
    cyl_shaft = up(head_height-0.1)(cylinder(h=length-head_height+0.1,
                                             r=shaft_r, segments=30))
    interior = rotate([90, 0, 0])(cyl_shaft+cyl_top)
    omg = hscrew-hole()(interior)
    # OMG HOLE is buggy; hscrew-=hole()(interior) does not always work
    return omg


def xulaconnector():
    screw_xuout = 2.5
    screw_xuin = 1.5
    screw_toph = 1
    offset = 5
    length = offset+THICK_WALL
    # XULA2 is attached to the top with two screws
    screw_xula = hscrew(screw_xuout, screw_toph, screw_xuin, length)
    screws_xula = screw_xula + right(58)(screw_xula)
    screws_xula += up(48.8)(screws_xula)
    xula_base = screws_xula
    # Raspberry connector xula2
    rsp_cnctr = cube([58-2*(screw_xuin+THICK_WALL*0.5), length, 6])
    xula_base += translate(
        [screw_xuin+THICK_WALL*0.5, -length, -3+48.8])(hole()(rsp_cnctr))
    # add stickit connector
    top_height = 4  # top height screw in mm
    top_r = 3.5  # top r screw in mm
    shaft_r = 2
    screw_stick = hscrew(top_r, top_height, shaft_r, length)
    screws_stick = screw_stick+up(15)(screw_stick)
    # stickit length 49.6-1.28-2-2
    # 15.5+1.5+1.2-1.5
    xula_base += translate([-(49.6-1.28-2-2)-8,
                            0, 15.5+1.5+1.2-1.5-2.7])(screws_stick)
    xula_base += translate([-60, -2, -8])(cube([123, 2, 61]))
    xula_base = up(THICK_WALL+11)(xula_base)
    # add down connector
    base_exit = cube([58+2*screw_xuin+THICK_WALL, 16, THICK_WALL])
    base_exit += hole()(translate([screw_xuin+THICK_WALL*0.5, THICK_WALL, 0])
                        (cube([58-2*(screw_xuin+THICK_WALL*0.5), 12, THICK_WALL])))
    xula_base += back(16)(base_exit)
    return xula_base


def topbox(down, logo):
    """topbox

    constructs the top part of the box
    :param down: if true downward ray box created
    :param logo: if true logo is generated, logo slows rendering
    """
    top = cube([LENGTH_TOP, WIDTH_TOP, THICK_WALL])
    # 4 screws used, 2 was insufficient
    screw_fixout = 3.5  # mm (radius)
    screw_fixin = 2  # TODO: connect to holesize threaded inserti
    screw_toph = 5
    cyl = screw(screw_fixout, screw_toph, screw_fixin, HEIGHT_TOP)
    top += translate([SCREW_FIXOFFST, SCREW_FIXOFFST, 0])(cyl)
    top += translate([LENGTH_TOP-SCREW_FIXOFFST, SCREW_FIXOFFST, 0])(cyl)
    top += translate([LENGTH_TOP-SCREW_FIXOFFST, WIDTH_TOP-SCREW_FIXOFFST, 0])(
        cyl)
    top += translate([SCREW_FIXOFFST, WIDTH_TOP-SCREW_FIXOFFST, 0])(cyl)

    # sliding should be prevented with 4 protrusion,
    # 1 is logo and 3 other are knobs
    x_knob = cube([THICK_WALL, THICK_WALL * 3, HEIGHT_TOP - THICK_WALL])
    x_knobs = translate([THICK_WALL, WIDTH_TOP/2-1, THICK_WALL])(
        x_knob)+translate([LENGTH_TOP-2*THICK_WALL, WIDTH_TOP/2-1, THICK_WALL])(
        x_knob)
    y_knob = cube([THICK_WALL*3, THICK_WALL, HEIGHT_TOP - THICK_WALL])
    y_knobs = translate([LENGTH_TOP*0.25, 0,
                         THICK_WALL])(forward(THICK_WALL)
                                      (y_knob)+forward(WIDTH_TOP-2*THICK_WALL)
                                      (y_knob))
    top += y_knobs + x_knobs
    # LOGO slows down render, should be turned off when developing
    if logo:
        top += translate([0.5*(LENGTH_TOP-(120+THICK_WALL*2)),
                          WIDTH_TOP-THICK_WALL-(13+THICK_WALL*2),
                          0])(createlogo())
    if not down:
        laser_y = 24 + 2 * THICK_WALL
        top -= translate([75+10+48+THICK_WALL+10, laser_y-0.5*8, 0])(
                cube([20, 8, THICK_WALL]))
    # FIX FOR BOX orientation
    top = rotate([0, 0, 180])(mirror([0, 1, 0])(rotate([0, 180, 0])(top)))

    return top


def boxmount():
    base = cube([30, 50, 2])
    circ = cylinder(h=10, r=1.6, segments=30)
    circs = right(5)(circ)+right(25)(circ)
    base -= forward(5)(circs)
    base -= forward(25)(circs)
    base -= forward(45)(circs)
    base = rotate([90, 0, 90])(base)
    return base


def onderkantbox(down):
    """onderkantbox

    constructs the bottom part of the box
    :param down: if true ray will be directed downward
    """
    # construct a base
    # height wall ; earlier experiments ; 40 (bottom) + 25 (top)
    height = 65
    base = cube([LENGTH_TOP, WIDTH_TOP, THICK_WALL+height])
    base -= translate([THICK_WALL, THICK_WALL, THICK_WALL])(cube(
        [LENGTH_TOP-2*THICK_WALL, WIDTH_TOP-2*THICK_WALL, height]))
    # NOTE the order in which objects are placed is important
    #     there can be coflicts between the stickit/panel mount and the
    #     mirror mount
    #     most likely this is due to the inner workings of the hole function

    # the polygon is the lowest part, for certainty its offset is set at
    # THICK_WALL laser_y = 24 (polygon) + 2 * THICK_WALL
    # as a result y-offset laserbase is  laser_y - 0.5 * 30 (width laserbase)
    # the y-offset mirror base=laser_y-0.5*light_hole-THICK_WALL-INSERT_MIRROR
    # the x-offset of the laserbase is 0,
    # it comes with an integrated ventilation
    # the x-offset of the polygon is  75 (length_base) + 10 (laserlens)
    # the x-offset mirror is 75 + 10 + 48 (width polygon) + THICK WALL (safety
    # margin) TODO: for an unknown reason the stickit nead to be added first
    #       other wise the photodiode mount will be effected
    # add stick
    base += translate([THICK_WALL + 90, WIDTH_TOP, 0])(
        xulaconnector())
    # add laser base
    laser_y = 24 + 2 * THICK_WALL
    base += translate([0, laser_y-0.5*30, 0])(laserbase(LASER_HEIGHT))
    # add polygon 4 is space for square
    base += translate([75+10+4, 2*THICK_WALL, 0])(polygonbase(LASER_HEIGHT))
    # add mirror; y position is corrected for mirror_insert,
    # thick wall +8 (square) and light hole
    base += translate([75 + 10 + 48 + THICK_WALL+8, laser_y,
                       0])(mirrormount(down, LASER_HEIGHT))

    # add exits DC barrels
    r_barrel = 6.6
    dcbarrel = rotate([90, 0, 0])(
        cylinder(r=r_barrel, h=2*THICK_WALL, segments=30))
    # NOTE: offset between DC barrels should
    #       be larger than radius due to extent
    base -= translate([THICK_WALL+r_barrel+10, WIDTH_TOP,
                       THICK_WALL+r_barrel*2])(
                           dcbarrel+up(2*r_barrel+4+THICK_WALL)(dcbarrel))
    # add exit for microusb (also has width of DC barrel)
    base -= translate([LENGTH_TOP-THICK_WALL, WIDTH_TOP-23.2,
                       THICK_WALL+11+23])(rotate([0, 0, 90])
                                          (dcbarrel))
    # add mount belt
    mount_box = cube([10, 30, 50])
    base -= translate([LENGTH_TOP-THICK_WALL, WIDTH_TOP-60, THICK_WALL+15])(
        mount_box)
    base += translate([LENGTH_TOP-THICK_WALL, WIDTH_TOP-60, THICK_WALL+15])(
        boxmount())
    # you need to create room mirror
    if down:
        # TODO: remove manual fixed parameters
        #        manual fix parameters; x 10 shift and y extent 20
        base -= translate([75+10+48+THICK_WALL+10, laser_y-0.5*light_hole, 0])(
            cube([20, light_hole, THICK_WALL]))

    # add two cable ties;
    #   corner
    # base += translate([LENGTH_TOP - 18, WIDTH_TOP - 10, THICK_WALL])
    #   (cable_fasten(TIE_HEIGHT, TIE_WIDTH, THICK_WALL, True))
    #   laserbase
    base += translate([75-10, WIDTH_TOP-20, THICK_WALL])(
        cable_fasten(TIE_HEIGHT, TIE_WIDTH, THICK_WALL, False))
    # add fasteners at corners
    #  bottom left and upper right corner
    upshift = THICK_WALL+height-HEIGHT_TOP+THICK_WALL
    base += translate([SCREW_FIXOFFST, SCREW_FIXOFFST, upshift])(
        threadedinsert(True, THICK_WALL, 4.0, 5.8))
    base += translate([LENGTH_TOP-SCREW_FIXOFFST, WIDTH_TOP-SCREW_FIXOFFST,
                       upshift])(threadedinsert(False, THICK_WALL, 4.0, 5.8))
    base += translate([LENGTH_TOP-SCREW_FIXOFFST, SCREW_FIXOFFST, upshift])(
        threadedinsert(True, THICK_WALL, 4.0, 5.8))
    base += translate([SCREW_FIXOFFST, WIDTH_TOP-SCREW_FIXOFFST, upshift])(
        threadedinsert(False, THICK_WALL, 4.0, 5.8))
    base = mirror([0, 1, 0])(base)
    return base


def renderparts():
    """
    renderparts

    renders all the subcomponents of the box
    placed in separate function to prevent collision
    """
    print_screw = screw(3, 2, 2, 10)  # create a printable screw
    scad_render_to_file(print_screw, 'print_screw.scad')

    print_lasershim = lasershim(1)
    scad_render_to_file(print_lasershim, 'shim.scad')

    print_laserbase = laserbase(LASER_HEIGHT)
    scad_render_to_file(print_laserbase, 'laserbase.scad')

    fasten = cable_fasten(TIE_HEIGHT, TIE_WIDTH, THICK_WALL, True)
    scad_render_to_file(fasten, 'cable_fasten.scad')

    print_insert = threadedinsert(True, THICK_WALL, 4.0, 5.8)
    scad_render_to_file(print_insert, 'print_insert.scad')

    print_polygonshim = polygonshim(1)
    scad_render_to_file(print_polygonshim, 'polygonshim.scad')

    print_polygonbase = polygonbase(LASER_HEIGHT)
    scad_render_to_file(print_polygonbase, 'polygonbase.scad')

    print_boxmount = boxmount()
    scad_render_to_file(print_boxmount, 'boxmount.scad')

    mirror_mount_down = mirrormount(True, LASER_HEIGHT)
    mirror_mount_down += back(20)(cube([30, 50, 2]))
    scad_render_to_file(mirror_mount_down, 'mirror_mount_down.scad')

    topdownr = topbox(True, False)
    scad_render_to_file(topdownr, 'topboxdown.scad')

    topupr = topbox(False, False)
    scad_render_to_file(topupr, 'topboxup.scad')

    top_height = 4  # top height screw in mm
    top_r = 3.5     # top r screw in mm for screw head
    shaft_r = 2    # screw radius
    offset = 5
    screw_length = THICK_WALL + offset

    print_hscrew = hscrew(top_r, top_height, shaft_r, 5+THICK_WALL)
    scad_render_to_file(print_hscrew, 'hscrew.scad')

    print_xulabase = xulaconnector()
    scad_render_to_file(print_xulabase, "xulabase.scad")
    # logo = createlogo()
    # scad_render_to_file(logo, 'logo.scad')

    panelmountr = panelmountmini()
    scad_render_to_file(panelmountr, 'panelmountmini.scad')

    onderkantdown = onderkantbox(True)
    scad_render_to_file(onderkantdown, 'onderkantdown.scad')

    onderkantup = onderkantbox(False)
    scad_render_to_file(onderkantup, 'onderkantup.scad')


if __name__ == "__main__":

    renderparts()

# STL FILES for printing
# TOP illumination
# TODO: error's is thrown, logo cannot be generated. Code is still usefull as
# the box generated is needed for subtraction logo
system("openscad -o "+"topboxdown.stl"+" topboxdown.scad")
# system("openscad -o "+"topboxup.stl"+" topboxup.scad")
system("openscad -o "+"onderkantdown.stl"+" onderkantdown.scad")
# system("openscad -o "+"onderkantup.stl"+" onderkantup.scad")

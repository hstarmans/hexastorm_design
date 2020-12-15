# Company: Hexastorm
# Author: Henri Starmans
# Date: 26-6-2017

from os import system
from math import sqrt, ceil
from solid.objects import cylinder, cube, polygon, import_stl, scale
from solid.utils import scad_render_to_file, up, back, right, translate
from solid.utils import rotate, left, down, mirror, forward, hole, linear_extrude, hull


THCKW = 2 # [mm], wall thickness
SGM = 30  # number of segment for circle


def ueyeholder():
    """ueyeholder
    creates a holder for an ueye camera

    A holder for an uEye camera to view upward.
    The uEye camera cannot look upward due its connector on the back.
    This design solves this problem via a cubical enclosure.
    """
    #### UEYE cubical dimension
    margin = 0.3
    size_x = 34        # mm
    size_y = 32        # mm
    size_z = 34.6      # mm
    ### UEYE screw
    screw_d = 3        # mm
    screw_z = 30.4     # sep z-direction
    screw_z -= screw_d
    screw_ytop = 19.8     # mm
    screw_ytop -= screw_d
    screw_ybottom = 21.8
    screw_ybottom -= screw_d
    screw_zoff = 1.3+screw_d/2
    connector_z = 18   # mm
    connector_x = 16.2 # mm
    #### 
    # box
    # camera is pushed in from bottom
    holder = cube([size_x+2*THCKW+margin, size_y+2*THCKW+margin, size_z+THCKW+connector_z+margin])
    holder -= translate([THCKW, THCKW , THCKW])(cube([size_x+margin, size_y+margin,
                                                      size_z+THCKW+connector_z+margin]))
    # 4 screw holes
    socket = cylinder(h=size_x+2*THCKW, r=screw_d/2, segments=SGM)
    socket = rotate([0,90,0])(socket)
    sockets = socket+forward(screw_ybottom)(socket)
    temp = (screw_ytop-screw_ybottom)*0.5
    sockets += up(screw_z)(back(temp)(socket)+forward(screw_ytop-temp)(socket))
    # substraction prep sockets
    holder -= translate([0, (size_y-screw_ybottom)*0.5+THCKW+0.5*margin,
                         screw_zoff+THCKW+connector_z+0.5*margin])(sockets)
    # space connector
    holder -=translate([THCKW+0.5*(size_x-connector_x),0,THCKW])(cube([connector_x,
                                                 THCKW,size_z+THCKW+connector_z]))
    return holder

if __name__ == "__main__":

    holder_print = ueyeholder()
    scad_render_to_file(holder_print, "holderprint.scad")


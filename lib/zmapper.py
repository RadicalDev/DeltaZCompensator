#======================================================================
# ZMapper - use a delta Z map (matrix) to adjust Z movements for each
# extrusion move and insert the Z into the line of code.
#
# Before: G1 X-4.24 Z34.4 E13.124
# After:  G1 X-4.24 Y29.08 Z34.4 E13.124
#
# The Z is the current layer height in mm plus the delta Z value at
# that X-Y position.
#
# USAGE: zmapper.py -i gcodefile.gcode -z heightmapfile.csv [-q]
#
# -q prevents the postprocessor from running, this way you can disable
# the script without deleting the postprocessor line.
#
# Copyright (C) 2015 Michael Hackney
#======================================================================
import array
import sys
import os
import string
import csv
import getopt

#---------------------------------------------------------------------------------------------
# basez is the current slice height, x and y are the postions from the center of the bed (0,0)
#
def getZ(heightMap, basez, x, y):
    X = x/10 + 14
    Y = y/10 + 14
    
    for row in heightMap:
        for e in row:
            print '%1.2f' % e,
        print "\n"
        
    print X
    print Y
    Z = basez + heightMap[X][Y]
    print Z

#---------------------------------------------------------------------------------------
# determine if the line is a begin layer section, if so, return the layer height (in mm)    
#
def find_begin_layer(line):
    if line.startswith('; BEGIN_LAYER_OBJECT z='):
        zIndex = line.find('z=')
        return line[zIndex+2:]
    return False

#-----------------------------------------------------------------------------------------------------
# determine if the line is a G1 move. If so, make sure it isn't a prime or Zlift (return False if so).
# If it's a normal extrusion move, return the line substrings.
#
def find_extrude_segment(line):
    # only process lines that start with a G1 movement
    if line.startswith('G1 X'):
        # make sure it isnt a prime or Z lift movement
        if 'Z' in line:
            return False
        lineParts = line.split()
        return lineParts

#--------------------------------------------------------------------------------------
# Use the X and Y positions in lineParts to lookup the Z height adjustment, add that to
# layerHeight and return a formatted gcode line.     
#
x_vals = []
y_vals = []
def mapZ(heightMap, columns, rows, lineParts, layerHeight):
    X = 0
    Y = 0
    for part in lineParts:
        firstChar = part[0]
        
        if firstChar == 'X':
            X = int(round(float(X)/10) + columns/2)
            if X not in x_vals:
                x_vals.append(X)

        elif firstChar == 'Y':
            Y = part[1:]
            Y = int(round(float(Y)/10) + rows/2)
            if Y not in y_vals:
                y_vals.append(Y)


    # Here's where I'd like to do a linear interpolation to get a better Z estimate.
    #
    deltaZ = heightMap[X][Y]
    newZ = float(deltaZ) + float(layerHeight)
    zLine = 'Z' + str(newZ)

    lineParts.insert(3, zLine.strip())
    newCodeLine = string.join(lineParts, " ")

    return newCodeLine

#--------------------------------------------------------------------------
# Read the delta Z matrix from a CSV file and create a two dimensional list
#
def makeDeltaZ(heightmap):
    with open(heightmap) as file:
        reader = csv.reader(file)
        htmap = list(reader)
        return htmap
                           
#====================================================
# __main__
#====================================================


def apply_map_to_gcode(gcodefn, heightfn, outfn=None):
    heightMap = makeDeltaZ(str(heightfn))
    columns = len(heightMap)
    rows = len(heightMap[0])
    print columns, rows
    if rows != columns:
        print "This program requires an NxN matrix"
        return False

    if not outfn:
        outfn = gcodefn + "-ZMapped"

    infile = open(gcodefn, 'rb')
    currentZ = 0
            
    with open(outfn, 'w') as outfile:
        outfile.write(';---------------------------------------')
        outfile.write("\n")    
        outfile.write('; Processed with ZMapper')
        outfile.write("\n")
        outfile.write(';---------------------------------------')
        outfile.write("\n")    
        
        for line in infile:
            layerHeight = find_begin_layer(line)

            if layerHeight:
                currentZ = layerHeight

            lineParts = find_extrude_segment(line)
            if lineParts:
                mappedLine = mapZ(heightMap, columns, rows, lineParts, currentZ)
                outfile.write(mappedLine)
                outfile.write("\n")
            else:
                outfile.write(line.replace('\r',''))
            
        infile.close()
        outfile.close()
    print x_vals
    print y_vals
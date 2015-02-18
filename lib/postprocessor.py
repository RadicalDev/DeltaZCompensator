__author__ = 'jfindley'
import os
import re

class PostProcessor(object):
    def __init__(self, gcode):
        if not os.path.exists(gcode):
            raise Exception("File not found: {0}".format(gcode))

        self.gcode = gcode
        self.interpolation_engine = None

    def set_interpolation_engine(self, engine):
        self.interpolation_engine = engine

class CuraPostProcessor(PostProcessor):
    def process(self, outfile=None):
        if not self.interpolation_engine:
            raise Exception("No interpolation engine specified")

        if not outfile:
            outfile, ext = os.path.splitext(self.gcode)
            outfile = outfile+"-processed"+ext

        layer_height = 0
        layer_count = 0
        with open(outfile, 'w') as out:
            with open(self.gcode, 'r') as gcode:
                for line in gcode:
                    line = line.strip()
                    if "LAYER" in line:
                        layer_count = int(line.split(":")[-1])
                    elif "G0" in line and "Z" in line:
                        layer_height = float(line[line.rindex("Z")+1:])
                    elif ("X" in line and "Y" in line and not "Z" in line):
                        try:
                            x, y = re.findall("(?:X|Y)(-?\d+(?:.\d+)?)", line)
                            z = self.interpolation_engine.get_z_offset(x, y, layer_height)
                            line = line + " Z{0} S1".format(z)
                        except Exception, e:
                            print "WARNING: Unrecognized movement line: ", line, " Error: ", e
                    out.write(line+"\n")

if __name__ == "__main__":
    pass
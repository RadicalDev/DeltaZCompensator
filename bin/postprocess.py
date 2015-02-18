__author__ = 'jfindley'
import os
import sys
sys.path.append(os.path.join("..", "lib"))

from interpolation import KDTreeInterpolationEngine
from postprocessor import CuraPostProcessor


if __name__ == "__main__":
    engine = KDTreeInterpolationEngine("../csv/zmap_2mm_z0.csv")
    processor = CuraPostProcessor("../gcode/test_circle.gcode")
    processor.set_interpolation_engine(engine)
    processor.process()

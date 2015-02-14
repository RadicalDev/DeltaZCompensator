__author__ = 'jfindley'
import os
import sys
sys.path.append(os.path.join("..", "lib"))

from interpolation import KDTreeInterpolationEngine
from postprocessor import CuraPostProcessor


if __name__ == "__main__":
    engine = KDTreeInterpolationEngine("../csv/zmap_3mm.csv")
    processor = CuraPostProcessor("../gcode/test_cura.gcode")
    processor.set_interpolation_engine(engine)
    processor.process()

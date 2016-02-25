from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import random
import unittest

from measurement_stats import angle
from measurement_stats import value
from measurement_stats import value2D

class test_value2D(unittest.TestCase):

    def test_angleBetween(self):
        p1 = value2D.Point2D(
            value.ValueUncertainty(2.0, 0.1),
            value.ValueUncertainty(0.0, 0.1) )
        p2 = value2D.Point2D(
            value.ValueUncertainty(0.0, 0.1),
            value.ValueUncertainty(2.0, 0.1) )

        a = p1.angle_between(p2)
        self.assertAlmostEquals(a.degrees, 90.0, 1)

    def test_rotate(self):
        HALF_SQRT_2 = 0.5*math.sqrt(2.0)
        HALF_SQRT_3 = 0.5*math.sqrt(3.0)

        tests = [
            (90.0, 0.0, 1.0), (-90.0, 0.0, -1.0),
            (180.0, -1.0, 0.0), (-180.0, -1.0, 0.0),
            (270.0, 0.0, -1.0), (-270.0, 0.0, 1.0),
            (360.0, 1.0, 0.0), (-360.0, 1.0, 0.0),
            (45.0, HALF_SQRT_2, HALF_SQRT_2),
            (-45.0, HALF_SQRT_2, -HALF_SQRT_2),
            (315.0, HALF_SQRT_2, -HALF_SQRT_2),
            (-315.0, HALF_SQRT_2, HALF_SQRT_2),
            (30.0, HALF_SQRT_3, 0.5), (-30.0, HALF_SQRT_3, -0.5),
            (330.0, HALF_SQRT_3, -0.5), (-330.0, HALF_SQRT_3, 0.5) ]

        for test in tests:
            radius = random.uniform(0.001, 1000.0)
            p = value2D.Point2D(
                value.ValueUncertainty(radius, 0.25),
                value.ValueUncertainty(0.0, 0.25) )

            p.rotate(angle.Angle(degrees=test[0]))
            self.assertAlmostEqual(p.x.raw, radius * test[1], 2)
            self.assertAlmostEqual(p.y.raw, radius * test[2], 2)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_value2D)
    unittest.TextTestRunner(verbosity=2).run(suite)






from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import numpy as np

from measurement_stats import density
from measurement_stats import value

def getAreaUnderCurve(xValues, yValues):
    area = 0.0
    for i in range(len(xValues) - 1):
        dx = xValues[i + 1] - xValues[i]
        area += dx*yValues[i]
    return area

class test_density(unittest.TestCase):

    def test_singleDensity(self):
        """ A single measurement value should have a total probability of
            unity
        """

        xValues = np.linspace(-10.0, 10.0, 100)
        measurements = [value.ValueUncertainty()]

        dist = density.Distribution(measurements=measurements)

        area = getAreaUnderCurve(xValues, dist.probabilities_at(xValues))
        self.assertAlmostEqual(area, 1.0, 3)

    def test_doubleDensityOverlap(self):
        """ Two overlapping measurement values should have a total probability
            of unity
        """
        xValues = np.linspace(-10.0, 10.0, 100)
        measurements = [value.ValueUncertainty(), value.ValueUncertainty()]

        dist = density.Distribution(measurements=measurements)
        area = getAreaUnderCurve(xValues, dist.probabilities_at(xValues))
        self.assertAlmostEqual(area, 1.0, 3)

    def test_doubleDensityOffset(self):
        """ Two measurements with different values and uncertainties should
            still result in a total probability of unity
        """

        xValues = np.linspace(-10.0, 25.0, 100)
        measurements = [
            value.ValueUncertainty(),
            value.ValueUncertainty(2.0, 2.0)
        ]

        dist = density.Distribution(measurements=measurements)
        area = getAreaUnderCurve(xValues, dist.probabilities_at(xValues))
        self.assertAlmostEqual(area, 1.0, 3)

    def test_singleDensityMedian(self):
        """ The median of a single measurement should be at the value of
            that measurement
        """

        for i in range(10):
            measurements = [value.ValueUncertainty.createRandom(-100, 100)]

            dist = density.Distribution(measurements=measurements)
            median = density.ops.percentile(dist)

            self.assertAlmostEqual(median['x'], measurements[0].value)
            self.assertAlmostEqual(median['target'], 0.5)

    def test_tukey_box(self):
        measurements = []
        while len(measurements) < 6:
            measurements.append(value.ValueUncertainty())

        dist = density.Distribution(measurements=measurements)
        unweighted = density.tukey.unweighted_boundaries(dist)
        weighted = density.tukey.weighted_boundaries(dist)

    def test_generalizedGetMedian(self):
        for i in range(10):
            measurements = [
                value.ValueUncertainty.createRandom(-100.0, -5.0),
                value.ValueUncertainty.createRandom(-500.0, -20.0),
                value.ValueUncertainty.createRandom(-100.0, -50.0),
                value.ValueUncertainty.createRandom(),
                value.ValueUncertainty.createRandom(),
                value.ValueUncertainty.createRandom()
            ]

            dist = density.Distribution(measurements=measurements)
            result = density.ops.percentile(dist)

    def test_overlap(self):
        d1 = density.Distribution(measurements=[value.ValueUncertainty()])
        d2 = density.Distribution(measurements=[value.ValueUncertainty()])
        self.assertAlmostEqual(density.ops.overlap(d1, d2), 1.0)

    def test_compareAgainstGaussian2(self):
        d1 = density.Distribution(measurements=[value.ValueUncertainty()])
        d2 = density.Distribution(
            measurements=[value.ValueUncertainty(uncertainty=0.5)]
        )
        self.assertLess(density.ops.overlap(d1, d2), 0.7)

    def test_compareAgainstGaussian3(self):
        d1 = density.Distribution(measurements=[value.ValueUncertainty()])
        d2 = density.Distribution(measurements=[
            value.ValueUncertainty(5.0),
            value.ValueUncertainty(8.0),
            value.ValueUncertainty(10.0, 2.0)
        ])

        self.assertGreaterEqual(density.ops.overlap(d1, d2), 0.0)
        self.assertLess(density.ops.overlap(d1, d2), 0.06)

    def test_fromValuesOnly(self):
        values = [11, 15, 3, 7, 2]
        dd = density.create_distribution(values)
        self.assertAlmostEqual(dd.minimum_value().value, min(*values))
        self.assertAlmostEqual(dd.maximum_value().value, max(*values))

    def test_getAdaptiveRange(self):
        dist = density.Distribution(measurements=[value.ValueUncertainty()])
        result = density.ops.adaptive_range(dist, 10.0)

    def test_getAdaptiveRangeMulti(self):
        measurements = [
            value.ValueUncertainty(),
            value.ValueUncertainty(2.0, 0.5) ]
        dist = density.Distribution(measurements=measurements)
        result = density.ops.adaptive_range(dist, 10.0)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_density)
    unittest.TextTestRunner(verbosity=2).run(suite)




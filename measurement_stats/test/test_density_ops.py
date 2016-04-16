from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from measurement_stats import value
from measurement_stats.density import distribution
from measurement_stats.density import ops


class TestDensityOps(unittest.TestCase):

    def test_weighted_mad(self):
        """
        """

        delta = 1.8

        measurements = []
        for index in range(10):
            measurements.append(value.ValueUncertainty(delta, 1.1))
            measurements.append(value.ValueUncertainty(-delta, 1.1))

        dist = distribution.Distribution(measurements)

        median = ops.percentile(dist, 0.5)['x']
        mad = ops.weighted_median_average_deviation(dist)

        self.assertAlmostEqual(median, 0, places=1)
        self.assertAlmostEqual(
            mad, delta,
            delta=0.5,
            msg='Median: {}'.format(median)
        )


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDensityOps)
    unittest.TextTestRunner(verbosity=2).run(suite)





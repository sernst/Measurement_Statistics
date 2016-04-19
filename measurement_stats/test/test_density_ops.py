from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from measurement_stats import value
from measurement_stats import distributions


class TestDensityOps(unittest.TestCase):

    def test_weighted_mad(self):
        """
        """

        delta = 1.8

        measurements = []
        for index in range(10):
            measurements.append(value.ValueUncertainty(delta, 1.1))
            measurements.append(value.ValueUncertainty(-delta, 1.1))

        dist = distributions.Distribution(measurements)

        median = distributions.distributions_ops.percentile(dist, 0.5)
        mad = distributions.distributions_ops.weighted_median_average_deviation(dist)

        self.assertAlmostEqual(median, 0, places=1)
        self.assertAlmostEqual(
            mad, delta,
            delta=0.5,
            msg='Median: {}'.format(median)
        )

    def test_percentiles(self):

        measurements = []
        for i in range(400):
            measurements.append(value.ValueUncertainty.create_random())

        dist = distributions.Distribution(measurements)

        self.assertAlmostEqual(
            0, distributions.distributions_ops.percentile(dist, count=6000),
            delta=0.075
        )


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDensityOps)
    unittest.TextTestRunner(verbosity=2).run(suite)





from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import measurement_stats as mstats


class TestDensity(unittest.TestCase):

    def test_no_overlap(self):
        """
        """

        dist = mstats.create_distribution([-2000], [1.0])
        comp = mstats.create_distribution([2000], [1.0])

        result = mstats.distributions.overlap2(dist, comp)
        self.assertAlmostEqual(result.value, 0)

    def test_low_overlap(self):
        """
        """

        values = [-10, 2, 20]
        uncertainties = [0.5, 0.5, 0.5]
        measurements = mstats.values.join(values, uncertainties)

        dist = mstats.create_distribution(measurements)
        comp = mstats.create_distribution(
            [mstats.mean.weighted_mean_and_deviation(measurements)]
        )

        result = mstats.distributions.overlap2(dist, comp)
        self.assertGreater(result.value, 0.3)

    def test_perfect_overlap(self):
        """ """

        values = [1, 1]
        uncertainties = [0.5, 0.5]
        measurements = mstats.values.join(values, uncertainties)

        dist = mstats.create_distribution(measurements)
        comp = mstats.create_distribution(
            [mstats.ValueUncertainty(values[0], uncertainties[0])]
        )

        result = mstats.distributions.overlap2(dist, comp)
        self.assertEqual(result.value, 1.0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDensity)
    unittest.TextTestRunner(verbosity=2).run(suite)




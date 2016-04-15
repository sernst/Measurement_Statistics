from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import unittest
import math

from measurement_stats import ops
from measurement_stats import mean
from measurement_stats import value


class TestBasics(unittest.TestCase):

    def test_isNumber(self):
        """test_isNumber doc..."""
        self.assertTrue(ops.is_number(1.234))
        self.assertTrue(ops.is_number(100))
        self.assertTrue(ops.is_number(-24))
        self.assertFalse(ops.is_number('12'))
        self.assertFalse(ops.is_number(self))

    def test_linearSpace(self):
        """test_linearSpace doc..."""

        result = ops.linear_space(0.0, 1.0, 10)
        self.assertTrue(len(result) == 10)
        self.assertAlmostEqual(0, result[0])
        self.assertAlmostEqual(1.0, result[-1])

        result = ops.linear_space(-25.0, 25.0, 51)
        self.assertTrue(len(result) == 51)
        self.assertAlmostEqual(-25.0, result[0])
        self.assertAlmostEqual(25.0, result[-1])

        try:
            self.assertTrue(result.index(0.0))
        except Exception:
            self.fail('Unexpected linear spacing')

    def test_roundToOrder(self):
        """test_roundToOrder doc..."""

        self.assertAlmostEqual(123.3, value.round_to_order(123.345, -1))

        # Using the round operator, which rounds 5 up when odd, down when even
        self.assertAlmostEqual(123.34, value.round_to_order(123.345, -2))
        self.assertAlmostEqual(123.36, value.round_to_order(123.355, -2))

        self.assertAlmostEqual(123, value.round_to_order(123.345, 0))
        self.assertAlmostEqual(120, value.round_to_order(123.345, 1))
        self.assertAlmostEqual(100, value.round_to_order(123.345, 2))

    def test_orderOfMagnitude(self):
        """test_orderOfMagnitude doc..."""
        testOrder = -9
        while testOrder < 10:
            for i in range(25):
                v  = random.uniform(1.0, 9.9)*math.pow(10.0, testOrder)
                result = value.order_of_magnitude(v)
                msg    = 'Invalid Order %s != %s (%s)' % (result, testOrder, v)
                self.assertEqual(testOrder, result,  msg)
            testOrder += 1

    def test_equivalent(self):
        """test_equivalent doc..."""
        self.assertTrue(value.equivalent(1.0, 1.001, 0.01))
        self.assertFalse(value.equivalent(1.0, 1.011, 0.01))

    def test_sqrtSumOfSquares(self):
        """test_sqrtSumOfSquares doc..."""
        self.assertEqual(1.0, ops.sqrt_sum_of_squares(-1.0))
        self.assertEqual(math.sqrt(2), ops.sqrt_sum_of_squares(1.0, 1.0))
        self.assertEqual(math.sqrt(4.25), ops.sqrt_sum_of_squares(2.0, 0.5))

    def test_toValueUncertainty(self):
        """test_toValueUncertainty doc..."""
        v = value.ValueUncertainty(math.pi, 0.00456)
        self.assertEqual(v.value, 3.142,
                         'Values do not match %s' % v.label)
        self.assertEqual(v.uncertainty, 0.005,
                         'Uncertainties do not match %s' % v.label)

        v = value.ValueUncertainty(100.0*math.pi, 42.0)
        self.assertEqual(v.value, 310.0, 'Values do not match %s' % v.label)
        self.assertEqual(v.uncertainty, 40.0,
                         'Uncertainties do not match %s' % v.label)

        v = value.ValueUncertainty(0.001*math.pi, 0.000975)
        self.assertEqual(v.value, 0.003, 'Values do not match %s' % v.label)
        self.assertEqual(v.uncertainty, 0.001,
                         'Uncertainties do not match %s' % v.label)

    def test_weightedAverage(self):
        """ doc... """
        values = [
            value.ValueUncertainty(11.0, 1.0),
            value.ValueUncertainty(12.0, 1.0),
            value.ValueUncertainty(10.0, 3.0) ]

        result = mean.weighted(*values)

        self.assertEqual(result.value, 11.4, 'Value Match')
        self.assertEqual(result.uncertainty, 0.7, 'Value Match')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasics)
    unittest.TextTestRunner(verbosity=2).run(suite)





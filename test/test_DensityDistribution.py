# test_DensityDistribution.py [UNIT TEST]
# (C) 2015
# Scott Ernst

from __future__ import \
    print_function, absolute_import, \
    unicode_literals, division

import unittest

import numpy as np

from refined_stats.ValueUncertainty import ValueUncertainty
from refined_stats.density import DensityDistribution

#_______________________________________________________________________________
def getAreaUnderCurve(xValues, yValues):
    area = 0.0
    for i in range(len(xValues) - 1):
        dx = xValues[i + 1] - xValues[i]
        area += dx*yValues[i]
    return area

#*******************************************************************************
class test_DensityDistribution(unittest.TestCase):

    #===========================================================================
    #                                                               C L A S S

    #___________________________________________________________________________
    def setUp(self):
        pass

    #___________________________________________________________________________
    def test_singleDensity(self):
        """ doc... """
        xValues = np.linspace(-10.0, 10.0, 100)
        values = [ValueUncertainty()]

        dd = DensityDistribution(values=values)
        result = dd.createDistribution(xValues)

        area = getAreaUnderCurve(xValues, result)
        self.assertAlmostEqual(area, 1.0, 3)

    #___________________________________________________________________________
    def test_doubleDensityOverlap(self):
        """ doc... """
        xValues = np.linspace(-10.0, 10.0, 100)
        values = [ValueUncertainty(), ValueUncertainty()]

        dd = DensityDistribution(values=values)
        result = dd.createDistribution(xValues)

        area = getAreaUnderCurve(xValues, result)
        self.assertAlmostEqual(area, 2.0, 3)

    #___________________________________________________________________________
    def test_doubleDensityOffset(self):
        """ doc... """
        xValues = np.linspace(-10.0, 25.0, 100)
        values = [ValueUncertainty(), ValueUncertainty(2.0, 2.0)]

        dd = DensityDistribution(values=values)
        result = dd.createDistribution(xValues)

        area = getAreaUnderCurve(xValues, result)
        self.assertAlmostEqual(area, 2.0, 3)

    #___________________________________________________________________________
    def test_singleDensityMedian(self):
        """ doc... """
        values = [ValueUncertainty()]

        dd = DensityDistribution(values=values)
        result = dd.getMedian()

        self.assertAlmostEqual(result.x, 0.0)
        self.assertAlmostEqual(result.target, 0.5)

    #___________________________________________________________________________
    def test_tukeyBox(self):
        values = [
            ValueUncertainty(), ValueUncertainty(),
            ValueUncertainty(), ValueUncertainty(),
            ValueUncertainty(), ValueUncertainty()]

        dd = DensityDistribution(values=values)
        result = dd.getTukeyBoxBoundaries()
        print(result)

    #___________________________________________________________________________
    def test_generalizedGetMedian(self):
        for i in range(2):
            values = [
                ValueUncertainty.createRandom(-100.0, -5.0),
                ValueUncertainty.createRandom(-500.0, -20.0),
                ValueUncertainty.createRandom(-100.0, -50.0),
                ValueUncertainty.createRandom(),
                ValueUncertainty.createRandom(),
                ValueUncertainty.createRandom() ]

            dd = DensityDistribution(values=values)
            result = dd.getMedian()
            print(result)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_DensityDistribution)
    unittest.TextTestRunner(verbosity=2).run(suite)




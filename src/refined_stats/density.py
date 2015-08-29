# density.py
# (C)2015
# Scott Ernst

from __future__ import \
    print_function, absolute_import, \
    unicode_literals, division

import math
import collections

import numpy as np

from refined_stats import numerics


################################################################################

def gaussianKernel(x, value):
    ave = value.value
    unc = value.uncertainty
    coefficient = 1/math.sqrt(2.0*math.pi*unc*unc)
    exponent = -0.5*((float(x) - ave)**2)/(unc*unc)
    return coefficient*math.exp(exponent)

#*******************************************************************************
class DensityDistribution(object):
    """A class for..."""

    MEDIAN_DATA_NT = collections.namedtuple(
        typename='MEDIAN_DATA_NT',
        field_names=['x', 'y', 'target'])

    #___________________________________________________________________________
    def __init__(self, **kwargs):
        """Creates a new instance of density."""
        self.values = kwargs.get('values', [])
        self.kernel = kwargs.get('kernel', gaussianKernel)

    #===========================================================================
    #                                                           G E T / S E T

    #___________________________________________________________________________
    @property
    def minimumValue(self):
        if not self.values:
            return None
        point = self.values[0]
        for v in self.values[1:]:
            if v.value == point.value and v.uncertainty > point.uncertainty:
                point = v
            elif v.value < point.value:
                point = v
        return point

    #___________________________________________________________________________
    @property
    def maximumValue(self):
        if not self.values:
            return None
        point = self.values[0]
        for v in self.values[1:]:
            if v.value == point.value and v.uncertainty > point.uncertainty:
                point = v
            elif v.value > point.value:
                point = v
        return point

    #===========================================================================
    #                                                             P U B L I C

    #___________________________________________________________________________
    def getUnweightedTukeyBoxBoundaries(self):
        vals = []
        for v in self.values:
            vals.append(v.value)

        median = np.percentile(vals, 50.0)
        lowerQuartile = np.percentile(vals, 25.0)
        upperQuartile = np.percentile(vals, 75.0)
        interquartileRange = upperQuartile - lowerQuartile
        return (
            lowerQuartile - interquartileRange,
            lowerQuartile,
            median,
            upperQuartile,
            upperQuartile + interquartileRange)

    #___________________________________________________________________________
    def getTukeyBoxBoundaries(self, tolerance = 0.0000001):
        median = self.getMedian(0.5)
        lowerQuartile = self.getMedian(0.25)
        upperQuartile = self.getMedian(0.75)
        interquartileRange = upperQuartile.x - lowerQuartile.x
        return (
            lowerQuartile.x - interquartileRange,
            lowerQuartile.x,
            median.x,
            upperQuartile.x,
            upperQuartile.x + interquartileRange)

    #___________________________________________________________________________
    def getMedian(self, target =0.5, tolerance = 0.0000001):
        xValues = self.getRange(sigmaPadding=10.0, numPoints=2048)

        total = float(len(self.values))
        area = 0.0
        x = xValues[0]
        dx = 0

        for i in range(len(xValues) - 1):
            x = xValues[i]
            xn = xValues[i + 1]
            dx = xn - x
            y = self.getValueAt(x)
            yn = self.getValueAt(xn)
            newArea = area + dx*(y + 0.5*(yn - y))

            test = newArea/total
            if numerics.equivalent(test, target, tolerance):
                return self.MEDIAN_DATA_NT(
                    x=xn,
                    y=yn,
                    target=test)

            elif test > target:
                break
            else:
                area = newArea

        areaNorm = area/total
        ratio = 0.5
        ratioMin = 0.0
        ratioMax = 1.0

        for i in range(10000):
            dxPiece = ratio*dx
            xn = x + dxPiece
            yn = self.getValueAt(xn)
            areaNormExtension = dxPiece*(y + 0.5*(yn - y))/total
            test = areaNorm + areaNormExtension

            if numerics.equivalent(test, target, tolerance):
                return self.MEDIAN_DATA_NT(
                    x=xn,
                    y=yn,
                    target=test)

            if test < target:
                 ratioMin = max(ratioMin, ratio)
            elif test > target:
                 ratioMax = min(ratioMax, ratio)

            ratio *= (target - areaNorm)/areaNormExtension
            if ratioMax <= ratio <= ratioMin:
                ratio = ratioMin + 0.5*(ratioMax - ratioMin)

        raise ValueError('Unable to find median value')

    #___________________________________________________________________________
    def getValuesAt(self, xValues):
        out = []
        for x in xValues:
            out.append(self.getValueAt(x))
        return out

    #___________________________________________________________________________
    def getValueAt(self, x):
        y = 0.0
        for v in self.values:
            y += self.kernel(x, v)
        return y

    #___________________________________________________________________________
    def createDistribution(self, xValues =None, normalize =False):
        """ doc..."""

        if xValues is None:
            xValues = self.getRange(2, numPoints=250)

        out = []
        for x in xValues:
            out.append(self.getValueAt(x))

        return out

    #___________________________________________________________________________
    def getMinimumBoundary(self, sigmaPadding):
        minVal = self.minimumValue
        return minVal.value - float(sigmaPadding)*minVal.uncertainty

    #___________________________________________________________________________
    def getMaximumBoundary(self, sigmaPadding):
        maxVal = self.maximumValue
        return maxVal.value + float(sigmaPadding)*maxVal.uncertainty

    #___________________________________________________________________________
    def getRange(self, sigmaPadding, numPoints =0, delta =0):
        minVal = self.getMinimumBoundary(sigmaPadding)
        maxVal = self.getMaximumBoundary(sigmaPadding)

        if not numPoints:
            if delta:
                numPoints = round((maxVal - minVal)/delta)
            else:
                numPoints = 1024

        return np.linspace(minVal, maxVal, int(numPoints))

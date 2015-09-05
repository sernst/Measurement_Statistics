# density.py
# (C)2015
# Scott Ernst

from __future__ import \
    print_function, absolute_import, \
    unicode_literals, division

import math
import random
import collections

import numpy as np
from pyaid.list.ListUtils import ListUtils
from pyaid.number.PositionValue2D import PositionValue2D
from pyaid.number.ValueUncertainty import ValueUncertainty

from refined_stats import numerics

################################################################################

def gaussianKernel(x, value):
    ave = value.value
    unc = value.uncertainty

    if x <= (ave - 10.0*unc) or x >= (ave + 10.0*unc):
        # Don't calculate values outside a "reasonable" range
        return 0.0

    if numerics.equivalent(unc, 0.0, 0.00000001):
        unc = 0.000001
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
        if not len(self.values):
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
        if not len(self.values):
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
    def getNumericValues(self, raw =False):
        out = []
        for v in self.values:
            out.append(v.raw if raw else v.value)
        return out

    #___________________________________________________________________________
    def compareAgainstGaussian(self, gaussianMean, gaussianStd):
        """ Returns the disparity in overlap between this distribution and a
            Gaussian one with the specified parameters. A value of 1.0 indicates
            that they overlap perfectly, while a value of 0.0 indicates that
            there is no overlap between the distributions. This approach can
            be useful in determining whether or not a distribution can be
            characterized by the specified Gaussian parameters.

        :param gaussianMean: float
        :param gaussianStd: float
        :return: overlap on range [0, 1.0]
        """
        compare = DensityDistribution(values=[
            ValueUncertainty(gaussianMean, gaussianStd)])

        xValues = self.getAdaptiveRange(10.0)
        for v in compare.getAdaptiveRange(10.0):
            if v not in xValues:
                xValues.append(v)
        xValues.sort()

        out = 0.0
        myValue = self.getValueAt(xValues[0])
        compareValue = compare.getValueAt(xValues[0])
        for i in range(len(xValues) - 1):
            x = xValues[i]
            xNext = xValues[i + 1]
            dx = xNext - x
            myNextValue = self.getValueAt(xNext)
            compareNextValue = compare.getValueAt(xNext)

            myArea = dx*(
                min(myValue, myNextValue) +
                0.5*abs(myNextValue - myValue)
            )/float(len(self.values))

            compareArea = dx*(
                min(compareValue, compareNextValue) +
                0.5*abs(compareNextValue - compareValue) )

            out += abs(myArea - compareArea)
            myValue = myNextValue
            compareValue = compareNextValue

        return 1.0 - 0.5*out

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
    def getDistributionPoints(self, count = 2048):
        out = []
        xMin = self.getMinimumBoundary(10)
        xMax = self.getMaximumBoundary(10)
        x = xMin
        delta = (xMax - xMin)/512.0
        total = float(len(self.values))
        while x <= xMax:
            n = int(round(count*delta*self.getValueAt(x)/total))
            for i in range(n):
                out.append(random.uniform(
                    x - 0.5*delta,
                    x + 0.5*delta))
            if x == xMax:
                break
            x = min(xMax, x + delta)
        return out

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
            newArea = area + dx*(y + 0.5*abs(yn - y))

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
            areaNormExtension = dxPiece*(y + 0.5*abs(yn - y))/total
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
    def createDistribution(
            self, xValues =None, normalize =False, asPoints =False
    ):
        """ doc..."""

        if xValues is None:
            xValues = self.getRange(2, numPoints=250)

        out = []
        for x in xValues:
            v = self.getValueAt(x)
            if asPoints:
                out.append(PositionValue2D(x=x, y=v))
            else:
                out.append(v)

        return out

    #___________________________________________________________________________
    def getMinimumBoundary(self, sigmaPadding):
        if not len(self.values):
            return 0.0
        v = self.values[0]
        b = v.value - float(sigmaPadding)*v.uncertainty
        for v in self.values[1:]:
            b = min(b, v.value - float(sigmaPadding)*v.uncertainty)
        return b

    #___________________________________________________________________________
    def getMaximumBoundary(self, sigmaPadding):
        if not len(self.values):
            return 0.0
        v = self.values[0]
        b = v.value + float(sigmaPadding)*v.uncertainty
        for v in self.values[1:]:
            b = max(b, v.value + float(sigmaPadding)*v.uncertainty)
        return b

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

    #___________________________________________________________________________
    def getAdaptiveRange(self, sigmaPadding, maximumDelta =None):
        minVal = self.getMinimumBoundary(sigmaPadding)
        maxVal = self.getMaximumBoundary(sigmaPadding)

        if maximumDelta is None:
            maximumDelta = 0.01*abs(maxVal - minVal)

        values = []
        for v in self.values:
            values.append({
                'min':v.value - 6.0*v.uncertainty,
                'max':v.value + 6.0*v.uncertainty,
                'value':v })
        values = ListUtils.sortDictionaryList(values, 'min')

        out = [minVal]
        while out[-1] < maxVal:
            delta = min(maximumDelta, maxVal - out[-1])
            xNext = out[-1] + delta

            index = 0
            while len(values) and index < len(values):
                v = values[index]
                x = out[-1]
                xNext = x + delta

                if xNext <= v['min']:
                    # BEFORE KERNEL: If the new x value is less than the lower
                    # bound of the kernel value, use that delta value.
                    break

                if v['max'] <= x:
                    # AFTER KERNEL: If x is higher than the kernel upper
                    # bound then skip to the next by removing this kernel from
                    # the list so that it won't appear in future iterations.
                    values.pop(0)
                    continue


                if v['min'] <= x <= v['max']:
                    # INSIDE KERNEL: If x is inside a kernel, use that kernel's
                    # delta if it is smaller than the delta already set.
                    delta = min(delta, 0.25*v['value'].uncertainty)

                elif x <= v['min'] and v['max'] <= xNext:
                    # OVER KERNEL: If x and x+dx wrap around the kernel, use
                    # a delta that puts the new x value at the lower edge of
                    # the kernel.
                    delta = min(delta, v['min'] - x)

                index += 1
                xNext = x + delta

            out.append(xNext)

        return out








    #___________________________________________________________________________
    @classmethod
    def fromValuesAndUncertainties(cls, values, uncertainties):
        data = []
        for i in range(len(values)):
            data.append(ValueUncertainty(values[i], uncertainties[i]))
        return DensityDistribution(values=data)

    #___________________________________________________________________________
    @classmethod
    def fromValuesAndUniformUncertainty(cls, values, uncertainty =1.0):
        data = []
        for i in range(len(values)):
            data.append(ValueUncertainty(values[i], uncertainty))
        return DensityDistribution(values=data)

    #___________________________________________________________________________
    @classmethod
    def fromMeanAndDeviation(cls, meanValue, stdValue):
        return DensityDistribution(values=[
            ValueUncertainty(meanValue, stdValue) ])

    #___________________________________________________________________________
    @classmethod
    def fromValuesOnly(cls, values):
        test = list(values) + []
        test.sort()

        deltas = []
        for i in range(len(test) - 1):
            deltas.append(abs(test[i] - test[i + 1]))
        m = max(0.00001, 0.5*float(np.median(deltas)))

        return cls.fromValuesAndUniformUncertainty(values, uncertainty=m)

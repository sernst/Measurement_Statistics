from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math


def gaussian(x, measurement, max_sigma = 10.0):
    """
    A Gaussian kernel function that returns a probability density value at
    the given x position where the Gaussian is defined by the center (mean)
    and width (standard deviation)

    :param x: Position where the kernel should be evaluated to return the
        probability density value
    :type: float

    :param measurement: A ValueUncertainty instance that is used to define
        the parameters for the kernel
    :type: value.ValueUncertainty

    :param max_sigma: The maximum amount of sigmas from the measurement value
        where the kernel will calculate the probability density. Any values
        outside of this threshold will just return a value of 0.
    :type: float:

    :return: The probability for the measurement at the given x position
    :rtype: float
    """

    center = measurement.value
    width = measurement.uncertainty

    width = max(width, 1e-6)

    if x <= (center - max_sigma * width) or x >= (center + max_sigma * width):
        # Don't calculate values outside a "reasonable" 10 sigma range
        return 0.0

    coefficient = 1 / math.sqrt(2.0 * math.pi * width * width)
    exponent = -0.5 * ((float(x) - center) ** 2) / (width * width)

    return coefficient * math.exp(exponent)

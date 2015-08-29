
import sys

#_______________________________________________________________________________
def equivalent(a, b, epsilon =None, machineEpsilonFactor =100.0):
    """equivalent doc..."""
    if epsilon is None:
        epsilon = machineEpsilonFactor*sys.float_info.epsilon
    return abs(float(a) - float(b)) < epsilon


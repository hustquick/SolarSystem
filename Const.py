"""This is a static class. It defines some constants and some common-used
functions.
DO NOT INITIALIZE IT!
"""
import math


def SIGMA():
    # Stefan–Boltzmann constant, W/(m^2 K^4)
    return 5.67e-8


def G():
    # Gravity of Earth, m/s^2
    return 9.807


def R():
    # Gas constant, J/(mol K)
    return 8.314


FLUID = {1: 'Water', 2: 'Air', 3: 'INCOMP::TVP1',
         4: 'Toluene', 5: 'R123'}


def logMean(a, b):
    if a * b > 0:
        return (a - b) / math.log(a / b)
    else:
        print("The two numbers are wrong!")
        return []


def convtemp(valuesToConvert, inputTempUnit, outputTempUnit):
    Unit = ['K', 'F', 'C', 'R']
    UnitSlope = {'K': 1, 'F': 5 / 9, 'C': 1, 'R': 5 / 9}
    UnitBias = {'K': 0, 'F': - 273.15 * 9 / 5 + 32, 'C': - 273.15, 'R': 0}

    if (inputTempUnit in Unit) and (outputTempUnit in Unit):
        return (valuesToConvert - UnitBias[inputTempUnit]) * \
                UnitSlope[inputTempUnit] / UnitSlope[outputTempUnit] \
                + UnitBias[outputTempUnit]
    else:
        raise ValueError("The units must be 'K', 'C',"
                         " 'F' or 'R'. Please check!")

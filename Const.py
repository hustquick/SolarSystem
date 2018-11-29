"""This is a static class. It defines some constants and some common-used
functions.
DO NOT INITIALIZE IT!
"""
import math


SIGMA = 5.67e-8
# Stefan–Boltzmann constant, W/(m^2 K^4)


G = 9.807
# Gravity of Earth, m/s^2


R = 8.314
# Gas constant, J/(mol K)


FLUID = {1: 'Water', 2: 'Air', 3: 'INCOMP::TVP1',
         4: 'Toluene', 5: 'R123'}


def logMean(a, b):
    if a * b > 0:
        return (a - b) / math.log(a / b)
    elif a * b < 0:
        return - (a + b) / math.log(- a / b)
    else:
        print("The two numbers are wrong!")
        return []


def convtemp(values_to_convert, input_temp_unit, output_temp_unit):
    unit = ['K', 'F', 'C', 'R']
    unit_slope = {'K': 1, 'F': 5 / 9, 'C': 1, 'R': 5 / 9}
    unit_bias = {'K': 0, 'F': - 273.15 * 9 / 5 + 32, 'C': - 273.15, 'R': 0}

    if (input_temp_unit in unit) and (output_temp_unit in unit):
        return (values_to_convert - unit_bias[input_temp_unit]) * \
                unit_slope[input_temp_unit] / unit_slope[output_temp_unit] \
                + unit_bias[output_temp_unit]
    else:
        raise ValueError("The units must be 'K', 'C',"
                         " 'F' or 'R'. Please check!")


def Nu_nat_conv(Gr, T_cav, T_amb, theta, d_ap, d_bar_cav):
    # This function describes the correlation of Nusselt number of the cavity
    S = - 0.982 * (d_ap / d_bar_cav) + 1.12
    return 0.088 * Gr ** (1/3) * (T_cav / T_amb) ** 0.18 \
        * (math.cos(theta)) ** 2.47 * (d_ap / d_bar_cav) ** S


def NuInPipe(Re, Pr, mu, mu_cav):
    # This is a function to get Nusselt number of forced convection in pipes:
    # The correlation can be found in the book.
    return 0.027 * Re ** 0.8 * Pr ** (1 / 3) * (mu / mu_cav) ** 0.14


def NuOfExternalCylinder(Re, Pr):
    # This is a function to get Nusselt number for flow perpendicular to
    # circular cylinder of diameter D, the average heat-transfer coefficient
    # can be obtained from the correlation in
    # BOOK "Process Heat Transfer PRINCIPLES AND APPLICATIONS".
    return 0.3 + 0.62 * Re ** (1/2) * Pr ** (1/3) / (1 + (0.4 / Pr) ** (2/3))\
           ** (1/4) * (1 + (Re / 282000) ** (5/8)) ** (4/5)


def NuOfExternalCylinder2(Re, Pr_1, Pr_2):
    if (0.7 < Pr_1 < 500) and (1 < Re < 10 ** 6):
        if Pr_1 > 10:
            n = 0.36
        else:
            n = 0.37
        if Re < 40:
            C = 0.75
            m = 0.4
        elif Re < 1000:
            C = 0.51
            m = 0.5
        elif Re < 20000:
            C = 0.26
            m = 0.6
        else:
            C = 0.076
            m = 0.7
    else:
        raise ValueError('Unproper Re number or Pr number')
    return C * Re ** m * Pr_1 ** n * (Pr_1/Pr_2) ** 0.25

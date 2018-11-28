"""This class describes the ambient class, including
parameters of solar direct irradience, temperature,
wind speed
"""
import Const

class Ambient:
    def __init__(self, I=700, T=288.15, P = 101325, wind_speed=4):
        self.I = I 		# Solar Direct Normal Irradiance， W/m^2
        self.fluid = Const.FLUID[2]
        self.T = T 	# Ambient temperature, K
        self.P = P      # Ambient Pressure, Pa
        self.wind_speed = wind_speed	# Ambient wind speed, m/s

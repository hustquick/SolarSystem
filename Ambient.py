"""This class describes the ambient class, including
parameters of solar direct irradiance, temperature,
wind speed
"""
import Const


class Ambient:
    def __init__(self, irradiance=700, temperature=288.15, pressure=101325, wind_speed=4):
        self.irradiance = irradiance 		# Solar Direct Normal Irradiance， W/m^2
        self.fluid = Const.FLUID[2]
        self.temperature = temperature 	# Ambient temperature, K
        self.pressure = pressure      # Ambient Pressure, Pa
        self.wind_speed = wind_speed  # Ambient wind speed, m/s

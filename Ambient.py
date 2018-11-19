"""This class describes the ambient class, including
parameters of solar direct irradience, temperature,
wind speed
"""
class Ambient:
    def __init__(self, I=700, T=288.15, wind_speed=1.5):
        self.I = I 		# Solar Direct Normal Irradiance， W/m^2
        self.T = T 	# Ambient temperature, K
        self.wind_speed = wind_speed	# Ambient wind speed, m/s

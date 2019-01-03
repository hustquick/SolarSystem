"""This class describes a fluid stream that has inherent
    properties and dependent properties
    For a stream, properties of fluid, temperature, pressure, quality can be set. Properties of h, s, u, cp
    are dependent and can not be set.
    Temperature, pressure, quality are interrelated. A flag `pressure_dependent` is set to identify whether the stream
    is pressure-dependent or temperature-dependent.
    """
from CoolProp.CoolProp import PropsSI as ps
import Const


class Stream:
    def __init__(self, fluid=Const.FLUID[1], flow_rate_value=0, pressure_dependent=True):
        self.fluid = fluid      # Fluid type
        self.flow_rate = [flow_rate_value]      # Mass flow rate, kg/s
        """Flow rate is a list so that it is object-based"""
        self._temperature = None          # Temperature, K
        self._pressure = None          # Pressure, Pa
        self._quality = None
        """Quality, [0, 1] for two phase stream; None for single
           phase stream
        """
        self.pressure_dependent = pressure_dependent
        # This is a flag to identify whether it is pressure-dependent or temperature-dependent

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature):
        if temperature < 0:
            raise ValueError("Temperature should be higher than 0 K!")
        if self.pressure_dependent:
            if (self._pressure is None) and (self._quality is not None):
                self._pressure = ps('P', 'Q', self._quality, 'T', float(temperature), self.fluid)
            elif (self._pressure is not None) and (self._quality is not None):
                raise ValueError("The stream is set to be pressure-dependent.\n"
                                 "Pressure and quality are already set, "
                                 "please check!")
        else:
            if self._quality is not None:
                self._pressure = ps('P', 'Q', self._quality, 'T', float(temperature), self.fluid)
        self._temperature = float(temperature)

    @property
    def temperature_celcius(self):
        return self._temperature - 273.15

    @temperature_celcius.setter
    def temperature_celcius(self, temperature_celcius):
        """You may choose to make the judgement by temperature setter and
        comment the lines below, and uncomment the last line
        """
        if temperature_celcius < -273.15:
            raise ValueError("Temperature should be higher than -273.15°C")
        if self.pressure_dependent:
            if (self._pressure is None) and (self._quality is not None):
                self._pressure = ps('P', 'Q', self._quality, 'T', float(temperature_celcius)+273.15, self.fluid)
            elif (self._pressure is not None) and (self._quality is not None):
                raise ValueError("The stream is set to be pressure-dependent.\n"
                                 "Pressure and quality are already set, "
                                 "please check!")
        else:
            if self._quality is not None:
                self._pressure = ps('P', 'Q', self._quality, 'T', float(temperature_celcius)+273.15, self.fluid)
        self._temperature = float(temperature_celcius) + 273.15
        # self.temperature = float(temperature_celcius) + 273.15

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, pressure):
        if pressure < 0:
            raise ValueError("Absolute pressure should be higher than 0 Pa!")
        if self.pressure_dependent:
            if self._quality is not None:
                self._temperature = ps('T', 'Q', self._quality, 'P', float(pressure), self.fluid)
        else:
            if (self._temperature is None) and (self._quality is not None):
                self._temperature = ps('T', 'Q', self._quality, 'P', float(pressure), self.fluid)
            elif (self._temperature is not None) and (self._quality is not None):
                raise ValueError("The stream is set to be temperature-dependent.\n"
                                 "Temperature and quality are already set, "
                                 "please check!")
        self._pressure = float(pressure)

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, quality):
        if quality is None:
            self._quality = None
        elif 0 <= quality <= 1:
            self._quality = float(quality)
            if self.pressure_dependent:
                if self._pressure is not None:
                    self._temperature = ps('T', 'Q', self._quality, 'P', self._pressure, self.fluid)
                elif (self._pressure is None) and (self._temperature is not None):
                    self._pressure = ps('P', 'Q', self.quality, 'T', self.temperature, self.fluid)
            else:
                if self._temperature is not None:
                    self._pressure = ps('P', 'Q', self.quality, 'T', self.temperature, self.fluid)
                elif (self._temperature is None) and (self._pressure is not None):
                    self._temperature = ps('T', 'Q', self._quality, 'P', self._pressure, self.fluid)
        else:
            raise ValueError("Wrong quality value!\nQuality should be a number between 0 and 1.")

    @property
    def h(self):
        return ps('H', 'T', self.temperature, 'P', self.pressure, self.fluid) if (self.quality is None) else \
               ps('H', 'P', self.pressure, 'Q', self.quality, self.fluid)

    @property
    def s(self):
        return ps('S', 'T', self._temperature, 'P', self.pressure, self.fluid) if (self.quality is None) else \
               ps('S', 'P', self.pressure, 'Q', self.quality, self.fluid)

    @property
    def u(self):
        return ps('U', 'T', self._temperature, 'P', self.pressure, self.fluid) if (self.quality is None) else \
            ps('U', 'P', self.pressure, 'Q', self.quality, self.fluid)

    @property
    def cp(self):
        return ps('C', 'T', self._temperature, 'P', self.pressure, self.fluid) \
            if (self.quality is None) else float("inf")

    def flow_to(self, stream):
        stream.fluid = self.fluid
        stream.flow_rate = self.flow_rate

    def mix(self, st1):
        st2 = Stream()
        if self.fluid == st1.fluid and self.pressure == st1.pressure:
            st2.fluid = self.fluid
            st2.pressure = self.pressure
            st2.flow_rate[0] = self.flow_rate[0] + st1.flow_rate[0]
            h = (self.flow_rate[0] * self.h + st1.flow_rate[0] * st1.h) / \
                (self.flow_rate[0] + st1.flow_rate[0])
            st2.temperature = ps('T', 'H', h, 'P', st2.pressure)
            return st2
        raise ValueError('Fluid types and pressures of the fluids'
                         'must be the same!')


if __name__ == '__main__':
    st = Stream()
    st.flow_rate = [2]
    st.pressure_dependent = False
    st.pressure = 1e5
    st.temperature_celcius = 200
    st.quality = 0.1
    # st.quality = None
    print(st.temperature)
    print(st.pressure)
    print(st.h)
    print(st.s)
    print(st.cp)

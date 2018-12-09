"""This class describes a fluid stream that has inherent
    properties and dependent properties
    For a stream, properties of fluid, temperature, pressure, x can be set. Properties of h, s, cp
    are dependent and can not be set.
    temperature, pressure, dryness are interrelated.
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
        self._dryness = None
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
            if (self._pressure is None) and (self._dryness is not None):
                self._pressure = ps('P', 'Q', self._dryness, 'T', float(temperature), self.fluid)
            elif (self._pressure is not None) and (self._dryness is not None):
                raise ValueError("The stream is set to be pressure-dependent.\n"
                                 "Pressure and quality are already set, "
                                 "please check!")
        else:
            if self._dryness is not None:
                self._pressure = ps('P', 'Q', self._dryness, 'T', float(temperature), self.fluid)
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
            if (self._pressure is None) and (self._dryness is not None):
                self._pressure = ps('P', 'Q', self._dryness, 'T', float(temperature_celcius)+273.15, self.fluid)
            elif (self._pressure is not None) and (self._dryness is not None):
                raise ValueError("The stream is set to be pressure-dependent.\n"
                                 "Pressure and quality are already set, "
                                 "please check!")
        else:
            if self._dryness is not None:
                self._pressure = ps('P', 'Q', self._dryness, 'T', float(temperature_celcius)+273.15, self.fluid)
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
            if self._dryness is not None:
                self._temperature = ps('T', 'Q', self._dryness, 'P', float(pressure), self.fluid)
        else:
            if (self._temperature is None) and (self._dryness is not None):
                self._temperature = ps('T', 'Q', self._dryness, 'P', float(pressure), self.fluid)
            elif (self._temperature is not None) and (self._dryness is not None):
                raise ValueError("The stream is set to be temperature-dependent.\n"
                                 "Temperature and quality are already set, "
                                 "please check!")
        self._pressure = float(pressure)

    @property
    def dryness(self):
        return self._dryness

    @dryness.setter
    def dryness(self, dryness):
        if dryness is None:
            self._dryness = None
        elif 0 <= dryness <= 1:
            self._dryness = float(dryness)
            if self.pressure_dependent:
                if self._pressure is not None:
                    self._temperature = ps('T', 'Q', self._dryness, 'P', self._pressure, self.fluid)
                elif (self._pressure is None) and (self._temperature is not None):
                    self._pressure = ps('P', 'Q', self.dryness, 'T', self.temperature, self.fluid)
            else:
                if self._temperature is not None:
                    self._pressure = ps('P', 'Q', self.dryness, 'T', self.temperature, self.fluid)
                elif (self._temperature is None) and (self._pressure is not None):
                    self._temperature = ps('T', 'Q', self._dryness, 'P', self._pressure, self.fluid)
        else:
            raise ValueError("Wrong dryness value!\nDryness should be a number between 0 and 1.")

    @property
    def h(self):
        return ps('H', 'T', self.temperature, 'P', self.pressure, self.fluid) if (self.dryness is None) else \
               ps('H', 'P', self.pressure, 'Q', self.dryness, self.fluid)

    @property
    def s(self):
        return ps('S', 'T', self._temperature, 'P', self.pressure, self.fluid) if (self.dryness is None) else \
               ps('S', 'P', self.pressure, 'Q', self.dryness, self.fluid)

    @property
    def cp(self):
        return ps('C', 'T', self._temperature, 'P', self.pressure, self.fluid) \
            if (self.dryness is None) else float("inf")

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
    st.dryness = 0.1
    # st.dryness = None
    print(st.temperature)
    print(st.pressure)
    print(st.h)
    print(st.s)
    print(st.cp)

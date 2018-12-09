"""This class define steam turbine
      The steam turbine is a product, N-6 2.35, of Qingdao Jieneng Power
      Station Engineering Co., Ltd
    """
from Stream import Stream
from CoolProp.CoolProp import PropsSI
import Const


class Turbine:
    _fluid_d = Const.FLUID[1]   # Designed working fluid
    _T_s_d = 663.15     # Designed main steam temperature, K
    _P_s_d = 2.35e6     # Designed main steam pressure, Pa
    _P_c_d = 1.5e4      # Designed exhaust pressure
    _dot_m_d = [32.09/3.6]    # Designed mass flow rate, kg/s
    _power_d = 6e6      # Designed power
    _alpha = 0.1        # dependency factor of stages. P13 of "Simulation of
    # the part-load behavior of a 30 MWe SEGES plant"

    def __init__(self, y=0, power=_power_d):
        self.st_i = Stream()
        self.st_o_1 = Stream()
        self.st_o_2 = Stream()
        self.y = y
        self._power = power

    @property
    def power(self):
        return self._power

    @power.getter
    def get_power(self):
        energy_in = self.st_i.flow_rate[0] * self.st_i.h
        energy_out = self.st_o_1.flow_rate[0] * self.y * self.st_o_1.h + \
            self.st_o_2.flow_rate[0] * (1 - self.y) * self.st_o_2.h
        self._power = energy_in - energy_out

    @power.setter
    def power(self, power):
        self._power = power

    @property
    def eta_i(self):
        enthalpy_drop = self._power_d / self._dot_m_d[0]
        h_i = PropsSI('H', 'T', self._T_s_d, 'P', self._P_s_d, self._fluid_d)
#        h_c = h_i - enthalpy_drop
        s_ideal = PropsSI('S', 'T', self._T_s_d, 'P', self._P_s_d,
                          self._fluid_d)
        h_c_ideal = PropsSI('H', 'S', s_ideal, 'P', self._P_c_d,
                            self._fluid_d)
        return enthalpy_drop / (h_i - h_c_ideal)

    def calculate_eta(self, p1, p2):
        return self.eta_i * (1 + self._alpha *
                             ((p1/self._P_s_d)/(p2/self._P_c_d) - 1) ** 2)

    def get_st2(self, st1, pressure2):
        st2 = Stream()
        st2.fluid = st1.fluid
        st2.flow_rate = st1.flow_rate
        st2.pressure = pressure2
        s_ideal = st1.s
        h2_ideal = PropsSI('H', 'S', s_ideal, 'P', st2.pressure, st2.fluid)
        eta = self.calculate_eta(st1.pressure, st2.pressure)
        h2 = st1.h - eta * (st1.h - h2_ideal)
        # Check whether it is saturated
        h2_l = PropsSI('H', 'P', st2.pressure, 'Q', 0, st2.fluid)
        h2_g = PropsSI('H', 'P', st2.pressure, 'Q', 1, st2.fluid)
        if h2_l <= h2 <= h2_g:
            st2.dryness = PropsSI('Q', 'P', st2.pressure, 'H', h2, st2.fluid)
        else:
            st2.temperature = PropsSI('T', 'P', st2.pressure, 'H', h2, st2.fluid)
        return st2


if __name__ == '__main__':
    tb = Turbine()

    tb.st_i.fluid = tb._fluid_d
    tb.st_i.pressure = tb._P_s_d
    tb.st_i.temperature = tb._T_s_d

    tb.st_o_2.fluid = tb._fluid_d
    tb.st_o_2.pressure = tb._P_c_d
    P1 = tb.st_i.pressure
    P2 = 20000
    st2 = tb.get_st2(tb.st_i, P2)


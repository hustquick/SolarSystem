"""This class describes a fluid stream that has inherent
    properties and dependent properties"""
from CoolProp.CoolProp import PropsSI
from mass_flow_rate import mass_flow_rate
import Const


class Stream:
    """This class describes a fluid stream that has inherent
    properties and dependent properties
    ATTENTION: If given T and P, set x will lead to change T, NOT P!
    Becasue in a power plant, the pressure is the controlled factor for
    mixed fluids.
    """
    def __init__(self, fluid=Const.FLUID[1], dot_m=mass_flow_rate(0)):
        self._T = None        # Temperature, K
        self._P = None         # Pressure, Pa
        self.fluid = fluid  # Fluid type
        self.dot_m = dot_m      # Mass flow rate, kg/s
        self.x = None
        """Quality, [0, 1] for two phase stream; NaN for single
        phase stream
        """

    @property
    def T(self):
        if (self.x is None) or (self.x <= 0) \
                or (self.x >= 1) or (self._P is None):
            return self._T
        else:
            return PropsSI('T', 'Q', self.x, 'P', self._P, self.fluid)

    @T.setter
    def T(self, T):
        if T < 0:
            raise ValueError("Temperature should be higher than 0 K!")
        if (self.x is None) or (self.x <= 0) \
                or (self.x >= 1) or (self._P is None):
            self._T = float(T)
        else:
            raise ValueError("Pressure and quality are already given,"
                             " please check!")

    @T.getter
    def get_T(self, h, P):
        if self.x is None:
            self._T = PropsSI('T', 'H', self.h, 'P', self.P, self.fluid)
        elif 0.0 <= self.x <= 1.0:
            self._T = PropsSI('T', 'Q', self.x, 'P', self.P, self.fluid)
        else:
            raise ValueError('Wrong quality number, x should be [0, 1]!')

    @property
    def T_c(self):
        if self.x is None:
            return self._T - 273.15
        elif 0.0 <= self.x <= 1.0:
            return PropsSI('T', 'P', self.P, 'Q', self.x, self.fluid) - 273.15
        else:
            raise ValueError('Wrong quality number, x should be [0, 1]!')

    @T_c.setter
    def T_c(self, T_c):
        if T_c < -273.15:
            raise ValueError("Temperature should be higher than -273.15°C")
        self._T = T_c + 273.15

    @property
    def P(self):
        if (self.x is None) or (self.x <= 0) \
                or (self.x >= 1) or (self._T is None):
            return self._P
        else:
            return PropsSI('P', 'Q', self.x, 'T', self.T, self.fluid)

    @P.setter
    def P(self, P):
        if P < 0:
            raise ValueError("Absolute pressure should be higher than 0 K!")
        if (self.x is None) or (self.x <= 0) \
                or (self.x >= 1) or (self.T is None):
            self._P = float(P)
        else:
            raise ValueError("Temperature and quality are already given,"
                             " please check!")

    @P.getter
    def get_P(self, h, P):
        if self.x is None:
            self._P = PropsSI('P', 'H', self.h, 'T', self._T, self.fluid)
        elif 0.0 <= self.x <= 1.0:
            self._P = PropsSI('P', 'Q', self.x, 'T', self._T, self.fluid)
        else:
            raise ValueError('Wrong quality number, x should be [0, 1]!')

    @property
    def h(self):
        if self.x is None:
            return PropsSI('H', 'T', self.T, 'P', self.P, self.fluid)
        elif 0.0 <= self.x <= 1.0:
            return PropsSI('H', 'P', self.P, 'Q', self.x, self.fluid)
        else:
            raise ValueError('Wrong quality number, x should be [0, 1]!')

    @property
    def s(self):
        if self.x is None:
            return PropsSI('S', 'T', self._T, 'P', self.P, self.fluid)
        elif 0.0 <= self.x <= 1.0:
            return PropsSI('S', 'P', self.P, 'Q', self.x, self.fluid)
        else:
            raise ValueError('Wrong quality number, x should be [0, 1]!')

    @property
    def cp(self):
        if self.x is None:
            return PropsSI('C', 'T', self._T, 'P', self.P, self.fluid)
        elif 0.0 <= self.x <= 1.0:
            return float("inf")
        else:
            raise ValueError('Wrong quality number, x should be [0, 1]!')

    def flow_to(self, st):
        st.fluid = self.fluid
        st.dot_m = self.dot_m

    def mix(self, st1):
        st2 = Stream()
        if self.fluid == st1.fluid and self.P == st1.P:
            st2.fluid = self.fluid
            st2.P = self.P
            st2.dot_m = self.dot_m + st1.dot_m
            h = (self.dot_m * self.h + st1.dot_m * st1.h) / \
                (self.dot_m + st1.dot_m)
            st2.T = PropsSI('T', 'H', h, 'P', st2.P)
            return st2
        raise ValueError('Fluid types and pressures of the fluids'
                         'must be the same!')


if __name__ == '__main__':
    st = Stream()
    st.T = 300
    st.P = 2e6
    st.x = 0.1
    print(st.T)
    print(st.P)

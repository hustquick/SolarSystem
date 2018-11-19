"""This class describes a fluid stream that has inherent
    properties and dependent properties"""
from CoolProp.CoolProp import PropsSI
import Const


class Stream:
    """This class describes a fluid stream that has inherent
    properties and dependent properties
    """

    def __init__(self, T=0, P=0, fluid=Const.FLUID[1]):
        self._T = T         # Temperature, K
        self.P = P          # Pressure, Pa
        self.fluid = fluid  # Fluid type
        self.dot_m = 0      # Mass flow rate, kg/s
        self.x = None
        """Quality, [0, 1] for two phase stream; NaN for single
        phase stream
        """

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, T):
        if T < 0:
            raise ValueError("Temperature should be higher than 0 K!")
        self._T = float(T)

    @T.getter
    def get_T(self, h, P):
        if self.x is None:
            self._T = PropsSI('T', 'H', self.h, 'P', self.P, self.fluid)
        elif 0.0 <= self.x <= 1.0:
            self._T = PropsSI('T', 'Q', 0, 'P', self.P, self.fluid)
        else:
            raise ValueError('Wrong quality number, x should be [0, 1]!')

    @property
    def T_c(self):
        return self._T - 273.15

    @T_c.setter
    def T_c(self, T_c):
        if T_c < -273.15:
            raise ValueError("Temperature should be higher than -273.15°C")
        self._T = T_c + 273.15

    @property
    def h(self):
        if self.x is None:
            return PropsSI('H', 'T', self._T, 'P', self.P, self.fluid)
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
    st = Stream(293.15, 1.01325e5)

"""This class describes a fluid stream that has inherent
    properties and dependent properties
    For a stream, properties of fluid, T, P, x can be set. Properties of h, s, cp
    are dependent and can not be set.
    T, P, x are interrelated.
    """
from CoolProp.CoolProp import PropsSI
from mass_flow_rate import mass_flow_rate
import Const


class Stream:
    def __init__(self, fluid=Const.FLUID[1], dot_m=mass_flow_rate(0), P_dependent=True):
        self.fluid = fluid      # Fluid type
        self.dot_m = dot_m      # Mass flow rate, kg/s
        self._T = None          # Temperature, K
        self._P = None          # Pressure, Pa
        self._x = None
        """Quality, [0, 1] for two phase stream; None for single
           phase stream
        """
        self.P_dependent = P_dependent  # This is a flag to identify whether it is P-dependent or T-dependent


    @property
    def T(self):
        if self.P_dependent:
            if (self.x is not None) and (self._P is not None):
                self._T = PropsSI('T', 'Q', self.x, 'P', self._P, self.fluid)
        return self._T

    @T.setter
    def T(self, T):
        if T < 0:
            raise ValueError("Temperature should be higher than 0 K!")
        if self.P_dependent:
            if (self.x is not None) and (self._P is not None):
                raise ValueError("The stream is set to be P-dependent.\n"
                                 "Pressure and quality are already given, "
                                 "please check!")
        self._T = float(T)

    @property
    def T_c(self):
        return self._T - 273.15

    @T_c.setter
    def T_c(self, T_c):
        if T_c < -273.15:
            raise ValueError("Temperature should be higher than -273.15°C")
        if self.P_dependent:
            if (self.x is not None) and (self._P is not None):
                raise ValueError("The stream is set to be P-dependent.\n"
                                 "Pressure and quality are already given, "
                                 "please check!")
        self._T = T_c + 273.15

    @property
    def P(self):
        if not self.P_dependent:
            if (self.x is not None) and (self._T is not None):
                self._P = PropsSI('P', 'Q', self.x, 'T', self.T, self.fluid)
        return self._P

    @P.setter
    def P(self, P):
        if P < 0:
            raise ValueError("Absolute pressure should be higher than 0 Pa!")
        if not self.P_dependent:
            if (self.x is not None) and (self._T is not None):
                raise ValueError("The stream is set to be T-dependent.\n"
                                 "Temperature and quality are already given, "
                                 "please check!")
        self._P = float(P)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if x is None:
            self._x = None
        elif 0 <= x <= 1:
            self._x = float(x)
        else:
            raise ValueError("Wrong x value!\nx should be a number between 0 and 1.")

    @property
    def h(self):
        return PropsSI('H', 'T', self.T, 'P', self.P, self.fluid) if (self.x is None) else \
               PropsSI('H', 'P', self.P, 'Q', self.x, self.fluid)

    @property
    def s(self):
        return PropsSI('S', 'T', self._T, 'P', self.P, self.fluid) if (self.x is None) else \
               PropsSI('S', 'P', self.P, 'Q', self.x, self.fluid)

    @property
    def cp(self):
        return PropsSI('C', 'T', self._T, 'P', self.P, self.fluid) if (self.x is None) else float("inf")

    def flow_to(self, st):
        st.fluid = self.fluid
        st.dot_m = self.dot_m

    def mix(self, st1):
        st2 = Stream()
        if self.fluid == st1.fluid and self.P == st1.P:
            st2.fluid = self.fluid
            st2.P = self.P
            st2.dot_m = self.dot_m.v + st1.dot_m.v
            h = (self.dot_m.v * self.h + st1.dot_m.v * st1.h) / \
                (self.dot_m.v + st1.dot_m.v)
            st2.T = PropsSI('T', 'H', h, 'P', st2.P)
            return st2
        raise ValueError('Fluid types and pressures of the fluids'
                         'must be the same!')


if __name__ == '__main__':
    st = Stream()
    st.T = 300
    st.x = 0
    # st.P_dependent = False
    st.P = 2e6

    st.P_dependent = False
    st.T_c = 100
    # Strange thing happened here. While debugging, it is found that st.P equals to 101418 here.
    st.x = None
    # when step over here, st.P is still 101418.
    # But! When set the breakpoint here, st.P will be 2e6.
    print(st.T)
    print(st.P)

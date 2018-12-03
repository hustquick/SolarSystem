"""This class describes a fluid stream that has inherent
    properties and dependent properties
    For a stream, properties of fluid, T, P, x can be set. Properties of h, s, cp
    are dependent and can not be set.
    T, P, x are interrelated.
    """
from CoolProp.CoolProp import PropsSI
import Const


class Stream:
    def __init__(self, fluid=Const.FLUID[1], dot_m=0, P_dependent=True):
        self.fluid = fluid      # Fluid type
        self.dot_m = [dot_m]      # Mass flow rate, kg/s
        self._T = None          # Temperature, K
        self._P = None          # Pressure, Pa
        self._x = None
        """Quality, [0, 1] for two phase stream; None for single
           phase stream
        """
        self.P_dependent = P_dependent  # This is a flag to identify whether it is P-dependent or T-dependent

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, T):
        if T < 0:
            raise ValueError("Temperature should be higher than 0 K!")
        if self.P_dependent:
            if (self._P is None) and (self._x is not None):
                self._P = PropsSI('P', 'Q', self._x, 'T', float(T), self.fluid)
            elif (self._P is not None) and (self._x is not None):
                raise ValueError("The stream is set to be P-dependent.\n"
                                 "Pressure and quality are already set, "
                                 "please check!")
        else:
            if self._x is not None:
                self._P = PropsSI('P', 'Q', self._x, 'T', float(T), self.fluid)
        self._T = float(T)

    @property
    def T_c(self):
        return self._T - 273.15

    @T_c.setter
    def T_c(self, T_c):
        """You may choose to make the judgement by T setter and
        comment the lines below, and uncomment the last line
        """
        if T_c < -273.15:
            raise ValueError("Temperature should be higher than -273.15°C")
        if self.P_dependent:
            if (self._P is None) and (self._x is not None):
                self._P = PropsSI('P', 'Q', self._x, 'T', float(T_c)+273.15, self.fluid)
            elif (self._P is not None) and (self._x is not None):
                raise ValueError("The stream is set to be P-dependent.\n"
                                 "Pressure and quality are already set, "
                                 "please check!")
        else:
            if self._x is not None:
                self._P = PropsSI('P', 'Q', self._x, 'T', float(T_c)+273.15, self.fluid)
        self._T = float(T_C) + 273.15
        # self.T = float(T_c) + 273.15

    @property
    def P(self):
        return self._P

    @P.setter
    def P(self, P):
        if P < 0:
            raise ValueError("Absolute pressure should be higher than 0 Pa!")
        if self.P_dependent:
            if self._x is not None:
                self._T = PropsSI('T', 'Q', self._x, 'P', float(P), self.fluid)
        else:
            if (self._T is None) and (self._x is not None):
                self._T = PropsSI('T', 'Q', self._x, 'P', float(P), self.fluid)
            elif (self._T is not None) and (self._x is not None):
                raise ValueError("The stream is set to be T-dependent.\n"
                                 "Temperature and quality are already set, "
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
            if self.P_dependent:
                if self._P is not None:
                    self._T = PropsSI('T', 'Q', self._x, 'P', self._P, self.fluid)
                elif (self._P is None) and (self._T is not None):
                    self._P = PropsSI('P', 'Q', self.x, 'T', self.T, self.fluid)
            else:
                if self._T is not None:
                    self._P = PropsSI('P', 'Q', self.x, 'T', self.T, self.fluid)
                elif (self._T is None) and (self._P is not None):
                    self._T = PropsSI('T', 'Q', self._x, 'P', self._P, self.fluid)
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

    def flow_to(self, stream):
        stream.fluid = self.fluid
        stream.dot_m = self.dot_m

    def mix(self, st1):
        st2 = Stream()
        if self.fluid == st1.fluid and self.P == st1.P:
            st2.fluid = self.fluid
            st2.P = self.P
            st2.dot_m[0] = self.dot_m[0] + st1.dot_m[0]
            h = (self.dot_m[0] * self.h + st1.dot_m[0] * st1.h) / \
                (self.dot_m[0] + st1.dot_m[0])
            st2.T = PropsSI('T', 'H', h, 'P', st2.P)
            return st2
        raise ValueError('Fluid types and pressures of the fluids'
                         'must be the same!')


if __name__ == '__main__':
    st = Stream()
    st.dot_m = [2]
    st.P_dependent = False
    st.P = 1e5
    st.T_c = 200
    st.x = 0.1
    # st.x = None
    print(st.T)
    print(st.P)
    print(st.h)
    print(st.s)
    print(st.cp)

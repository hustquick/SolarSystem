from Stream import Stream
from CoolProp.CoolProp import PropsSI
import Const


class HeatExchanger:
    """This class defines heat exchangers
        st1 is hot fluid, st2 is cold fluid
    """
    st1_pip = None
    st2_pip = None

    def __init__(self, eta=1):
        self.st1_i = Stream()
        self.st1_o = Stream()
        self.st2_i = Stream()
        self.st2_o = Stream()
        self.eta = eta

    def pressure_drop(self, st, pip):
        # 等待修改
        return 0 * st * pip * self.eta

    def calc_st1_i(self):
        st1_i = Stream()
        st1_i.fluid = self.st1_o.fluid
        st1_i.flow_rate = self.st1_o.flow_rate
        st1_i.pressure = self.st1_o.pressure + self.pressure_drop(self.st1_o, self.st1_pip)
        h = self.st1_o.h + (self.st2_i.h - self.st2_o.h) * self.st2_i.flow_rate[0] \
            / self.st1_o.flow_rate[0] / self.eta
        h_l = PropsSI('H', 'P', st1_i.pressure, 'Q', 0, st1_i.fluid)
        h_g = PropsSI('H', 'P', st1_i.pressure, 'Q', 1, st1_i.fluid)
        if h_l <= h <= h_g:
            st1_i.quality = PropsSI('Q', 'P', st1_i.pressure, 'H', h,
                                    st1_i.fluid)
        else:
            st1_i.temperature = PropsSI('T', 'P', st1_i.pressure, 'H', h,
                                        st1_i.fluid)
        self.st1_i = st1_i

    def calc_st1_o(self):
        st1_o = Stream()
        st1_o.fluid = self.st1_i.fluid
        st1_o.flow_rate = self.st1_i.flow_rate
        st1_o.pressure = self.st1_i.pressure - self.pressure_drop(self.st1_i, self.st1_pip)
        h = self.st1_i.h - (self.st2_i.h - self.st2_o.h) * self.st2_i.flow_rate[0] \
            / st1_o.flow_rate[0] / self.eta
        h_l = PropsSI('H', 'P', st1_o.pressure, 'Q', 0, st1_o.fluid)
        h_g = PropsSI('H', 'P', st1_o.pressure, 'Q', 1, st1_o.fluid)
        if h_l <= h <= h_g:
            st1_o.quality = PropsSI('Q', 'P', st1_o.pressure, 'H', h,
                                    st1_o.fluid)
        else:
            st1_o.T = PropsSI('T', 'P', st1_o.pressure, 'H', h,
                              st1_o.fluid)
        self.st1_o = st1_o

    def calc_st2_i(self):
        st2_i = Stream()
        st2_i.fluid = self.st2_o.fluid
        st2_i.flow_rate = self.st2_o.flow_rate
        st2_i.pressure = self.st2_o.pressure + self.pressure_drop(self.st2_o, self.st2_pip)
        h = self.st2_o.h + (self.st1_i.h - self.st1_o.h) * self.st1_i.flow_rate[0] \
            / self.st2_o.flow_rate[0] * self.eta
        h_l = PropsSI('H', 'P', st2_i.pressure, 'Q', 0, st2_i.fluid)
        h_g = PropsSI('H', 'P', st2_i.pressure, 'Q', 1, st2_i.fluid)
        if h_l <= h <= h_g:
            st2_i.x = PropsSI('Q', 'P', st2_i.pressure, 'H', h,
                                   st2_i.fluid)
        else:
            st2_i.T = PropsSI('T', 'P', st2_i.pressure, 'H', h,
                                   self.st2_i.fluid)
        self.st2_i = st2_i

    def calc_st2_o(self):
        st2_o = Stream()
        st2_o.fluid = self.st2_i.fluid
        st2_o.flow_rate = self.st2_i.flow_rate
        st2_o.pressure = self.st2_i.pressure - self.pressure_drop(self.st2_i, self.st2_pip)
        h = self.st2_i.h - (self.st1_i.h - self.st1_o.h) * self.st1_i.flow_rate[0] \
            / st2_o.flow_rate[0] / self.eta
        h_l = PropsSI('H', 'P', st2_o.pressure, 'Q', 0, st2_o.fluid)
        h_g = PropsSI('H', 'P', st2_o.pressure, 'Q', 1, st2_o.fluid)
        if h_l <= h <= h_g:
            st2_o.x = PropsSI('Q', 'P', st2_o.pressure, 'H', h,
                              st2_o.fluid)
        else:
            st2_o.temperature = PropsSI('T', 'P', st2_o.pressure, 'H', h,
                                        st2_o.fluid)
        self.st2_o = st2_o


if __name__ == '__main__':
    he = HeatExchanger()
    he.st1_o.fluid = 'water'
    he.st1_o.temperature = 700
    he.st1_o.pressure = 1e5
    he.st1_o.flow_rate[0] = 1

    he.st2_i.fluid = Const.FLUID[1]
    he.st2_i.temperature = 500
    he.st2_i.pressure = 1e5
    he.st2_i.flow_rate[0] = 2

    he.st2_o.fluid = he.st2_i.fluid
    he.st2_o.temperature = 400
    he.st2_o.pressure = 1e5
    he.st2_o.flow_rate[0] = 3

    he.calc_st1_i()
    he.calc_st1_o()
    he.calc_st2_i()
    he.calc_st2_o()

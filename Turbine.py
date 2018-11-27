from mass_flow_rate import mass_flow_rate
from Stream import Stream
from CoolProp.CoolProp import PropsSI
import Const


class Turbine:
    """This class define steam turbine
      The steam turbine is a product, N-6 2.35, of Qingdao Jieneng Power
      Station Engineering Co., Ltd
    """
    _fluid_d = Const.FLUID[1]   # Designed working fluid
    _T_s_d = 663.15     # Designed main steam temperature, K
    _P_s_d = 2.35e6     # Designed main steam pressure, Pa
    _P_c_d = 1.5e4      # Designed exhaust pressure
    _dot_m_d = mass_flow_rate(32.09/3.6)    # Designed mass flow rate
    _power_d = 6e6      # Designed power
    _alpha = 0.1        # dependancy factor of stages. P13 of "Simulation of
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
        energy_in = self.st_i.dot_m * self.st_i.h
        energy_out = self.st_o_1.dot_m * self.y * self.st_o_1.h + \
            self.st_o_2.dot_m * (1 - self.y) * self.st_o_2.h
        self._power = energy_in - energy_out

    @power.setter
    def set_power(self, power):
        self._power = power

    @property
    def eta_i(self):
        enthalpy_drop = self._power_d / self._dot_m_d.v
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

    def get_st2(self, st1, P2):
        st2 = Stream()
        st2.fluid = st1.fluid
        st2.dot_m = st1.dot_m
        st2.P = P2
        s_ideal = st1.s
        h2_ideal = PropsSI('H', 'S', s_ideal, 'P', st2.P, st2.fluid)
        eta = self.calculate_eta(st1.P, st2.P)
        h2 = st1.h - eta * (st1.h - h2_ideal)
        # Check whether it is saturated
        h2_l = PropsSI('H', 'P', st2.P, 'Q', 0, st2.fluid)
        h2_g = PropsSI('H', 'P', st2.P, 'Q', 1, st2.fluid)
        if h2_l <= h2 <= h2_g:
            st2.x = PropsSI('Q', 'P', st2.P, 'H', h2, st2.fluid)
        else:
            st2.T = PropsSI('T', 'P', st2.P, 'H', h2, st2.fluid)
        return st2


if __name__ == '__main__':
    tb = Turbine()

    tb.st_i.fluid = tb._fluid_d
    tb.st_i.P = tb._P_s_d
    tb.st_i.T = tb._T_s_d

    tb.st_o_2.fluid = tb._fluid_d
    tb.st_o_2.P = tb._P_c_d
    P1 = tb.st_i.P
    P2 = 20000
    st2 = tb.get_st2(tb.st_i, P2)


#    properties(Dependent)
#        P;      % Power of steam turbine, W
#        eta_i;    % Efficiency of the turbine
#    end
#
#    methods
#        function obj = Turbine
#            obj.st_i = Stream;
#            obj.st_o_1 = Stream;
#            obj.st_o_2 = Stream;
#        end
#    end
#    methods
#        function flowInTurbine(obj, st1, st2, p)
#            st2.fluid = st1.fluid;
#            st2.q_m = st1.q_m;
#            st2.p = p;
#            h2_i = CoolProp.PropsSI('H', 'P', st2.p.v, 'S', st1.s, st2.fluid);
#            h2 = st1.h - obj.eta_i .* (st1.h - h2_i);
#            h2_l = CoolProp.PropsSI('H', 'P', st2.p.v, 'Q', 0, st2.fluid);
#            h2_g = CoolProp.PropsSI('H', 'P', st2.p.v, 'Q', 1, st2.fluid);
#            if (h2 >= h2_l && h2 <= h2_g)
#%                 st2.x = (h2 - h2_l) ./ (h2_g - h2_l);
#                st2.x = CoolProp.PropsSI('Q', 'P', st2.p.v, ...
#                    'H', h2, st2.fluid);
#                st2.T = CoolProp.PropsSI('T', 'P', st2.p.v, ...
#                    'Q', st2.x, st2.fluid);
#            else
#                st2.T = CoolProp.PropsSI('T', 'P', st2.p.v,'H', ...
#                    h2, st2.fluid);
#            end
#        end
#        function work(obj, ge)
#            st_tmp1 = Stream;
#            st_tmp2 = Stream;
#            obj.flowInTurbine(obj.st_i, st_tmp1, obj.st_o_1.p);
#            obj.flowInTurbine(st_tmp1, st_tmp2, obj.st_o_2.p);
#            P = ge.P ./ ge.eta;
#            y1 = (P - obj.st_i.q_m.v .* (obj.st_i.h - st_tmp2.h)) ...
#                / (obj.st_i.q_m.v .* (st_tmp2.h - st_tmp1.h));
#            if (y1 >= 0 && y1 <= 1)
#                obj.y = y1;
#                st_tmp1.convergeTo(obj.st_o_1, obj.y);
#                st_tmp2.convergeTo(obj.st_o_2,1 - obj.y);
#            else
#                error('wrong y value of turbine');
#%                 obj.y = 1;
#%                 st_tmp1.convergeTo(obj.st_o_1, obj.y);
#%                 st_tmp2.convergeTo(obj.st_o_2,1 - obj.y);
#            end
#        end
#        function value = get_q_m(obj, ge)
#            P = ge.P ./ ge.eta;
#            st_tmp1 = Stream;
#            st_tmp2 = Stream;
#            obj.flowInTurbine(obj.st_i, st_tmp1, obj.st_o_1.p);
#            obj.flowInTurbine(st_tmp1, st_tmp2, obj.st_o_2.p);
#
#            delta_h = obj.st_i.h - obj.y .* ...
#                st_tmp1.h - (1 - obj.y) .* st_tmp2.h;
#            value = P / delta_h;
#        end
#
#        function value = get.eta_i(obj)
#            h_1_d = CoolProp.PropsSI('H', 'T', obj.T_s_d, 'P', ...
#                obj.p_s_d, obj.fluid_d);
#            s_1_d = CoolProp.PropsSI('S', 'T', obj.T_s_d, 'P', ...
#                obj.p_s_d, obj.fluid_d);
#            h_2_d = h_1_d - obj.P_d / obj.q_m_d.v;
#            h_2_i_d = CoolProp.PropsSI('H', 'S', s_1_d, 'P', ...
#                obj.p_c_d, obj.fluid_d);
#            value = (h_1_d - h_2_d) / (h_1_d - h_2_i_d);
#        end
#        function value = get.P(obj)
#            value = obj.st_i.q_m.v .* ((1-obj.y) .* ...
#                (obj.st_i.h - obj.st_o_2.h) + ...
#                obj.y .* (obj.st_i.h - obj.st_o_1.h));
#        end
#    end
#end
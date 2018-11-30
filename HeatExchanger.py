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
        return 0

    def calc_st1_i(self):
        st1_i = Stream()
        st1_i.fluid = self.st1_o.fluid
        st1_i.dot_m = self.st1_o.dot_m
        st1_i.P = self.st1_o.P + self.pressure_drop(self.st1_o, self.st1_pip)
        h = self.st1_o.h + (self.st2_i.h - self.st2_o.h) * self.st2_i.dot_m[0] \
            / self.st1_o.dot_m[0] / self.eta
        h_l = PropsSI('H', 'P', st1_i.P, 'Q', 0, st1_i.fluid)
        h_g = PropsSI('H', 'P', st1_i.P, 'Q', 1, st1_i.fluid)
        if h_l <= h <= h_g:
            st1_i.x = PropsSI('Q', 'P', st1_i.P, 'H', h,
                                   st1_i.fluid)
        else:
            st1_i.T = PropsSI('T', 'P', st1_i.P, 'H', h,
                                   self.st1_i.fluid)
        self.st1_i = st1_i

    def calc_st1_o(self):
        st1_o = Stream()
        st1_o.fluid = self.st1_i.fluid
        st1_o.dot_m = self.st1_i.dot_m
        st1_o.P = self.st1_i.P - self.pressure_drop(self.st1_i, self.st1_pip)
        h = self.st1_i.h - (self.st2_i.h - self.st2_o.h) * self.st2_i.dot_m[0] \
            / st1_o.dot_m[0] / self.eta
        h_l = PropsSI('H', 'P', st1_o.P, 'Q', 0, st1_o.fluid)
        h_g = PropsSI('H', 'P', st1_o.P, 'Q', 1, st1_o.fluid)
        if h_l <= h <= h_g:
            st1_o.x = PropsSI('Q', 'P', st1_o.P, 'H', h,
                                   st1_o.fluid)
        else:
            st1_o.T = PropsSI('T', 'P', st1_o.P, 'H', h,
                                   st1_o.fluid)
        self.st1_o = st1_o

    def calc_st2_i(self):
        st2_i = Stream()
        st2_i.fluid = self.st2_o.fluid
        st2_i.dot_m = self.st2_o.dot_m
        st2_i.P = self.st2_o.P + self.pressure_drop(self.st2_o, self.st2_pip)
        h = self.st2_o.h + (self.st1_i.h - self.st1_o.h) * self.st1_i.dot_m[0] \
            / self.st2_o.dot_m[0] * self.eta
        h_l = PropsSI('H', 'P', st2_i.P, 'Q', 0, st2_i.fluid)
        h_g = PropsSI('H', 'P', st2_i.P, 'Q', 1, st2_i.fluid)
        if h_l <= h <= h_g:
            st2_i.x = PropsSI('Q', 'P', st2_i.P, 'H', h,
                                   st2_i.fluid)
        else:
            st2_i.T = PropsSI('T', 'P', st2_i.P, 'H', h,
                                   self.st2_i.fluid)
        self.st2_i = st2_i

    def calc_st2_o(self):
        st2_o = Stream()
        st2_o.fluid = self.st2_i.fluid
        st2_o.dot_m = self.st2_i.dot_m
        st2_o.P = self.st2_i.P - self.pressure_drop(self.st2_i, self.st2_pip)
        h = self.st2_i.h - (self.st1_i.h - self.st1_o.h) * self.st1_i.dot_m[0] \
            / st2_o.dot_m[0] / self.eta
        h_l = PropsSI('H', 'P', st2_o.P, 'Q', 0, st2_o.fluid)
        h_g = PropsSI('H', 'P', st2_o.P, 'Q', 1, st2_o.fluid)
        if h_l <= h <= h_g:
            st2_o.x = PropsSI('Q', 'P', st2_o.P, 'H', h,
                                   st2_o.fluid)
        else:
            st2_o.T = PropsSI('T', 'P', st2_o.P, 'H', h,
                                   st2_o.fluid)
        self.st2_o = st2_o


#    methods
#        function get_st1_i(obj)
#            % Calculate inlet properties of stream 1
#            obj.st1_i.fluid = obj.st1_o.fluid;
#            obj.st1_i.q_m = obj.st1_o.q_m;
#            obj.st1_i.p = obj.st1_o.p;
#            h = obj.st1_o.h - (obj.st2_i.h - obj.st2_o.h) ...
#                .* obj.st2_i.q_m.v ./ obj.st1_i.q_m.v;
#
#            h_l = CoolProp.PropsSI('H', 'P', obj.st1_i.p.v, 'Q', 0, obj.st1_i.fluid);
#            h_g = CoolProp.PropsSI('H', 'P', obj.st1_i.p.v, 'Q', 1, obj.st1_i.fluid);
#            if (h >= h_l && h <= h_g)
#                obj.st1_i.x = CoolProp.PropsSI('Q', 'P', obj.st1_i.p.v, ...
#                    'H', h, obj.st1_i.fluid);
#                obj.st1_i.T = CoolProp.PropsSI('T', 'P', obj.st1_i.p.v, ...
#                    'Q', obj.st1_i.x, obj.st1_i.fluid);
#            else
#                obj.st1_i.T = CoolProp.PropsSI('T', 'P', obj.st1_i.p.v, ...
#                    'H', h, obj.st1_i.fluid);
#            end
#        end
#        function get_st1_o(obj)
#            % Calculate outlet properties of stream 1
#            obj.st1_o.fluid = obj.st1_i.fluid;
#            obj.st1_o.q_m = obj.st1_i.q_m;
#            obj.st1_o.p = obj.st1_i.p;
#            h = obj.st1_i.h + (obj.st2_i.h - obj.st2_o.h) ...
#                .* obj.st2_i.q_m.v ./ obj.st1_i.q_m.v;
#            h_l = CoolProp.PropsSI('H', 'P', obj.st1_o.p.v, 'Q', 0, obj.st1_o.fluid);
#            h_g = CoolProp.PropsSI('H', 'P', obj.st1_o.p.v, 'Q', 1, obj.st1_o.fluid);
#            if (h >= h_l && h <= h_g)
#                obj.st1_o.x = CoolProp.PropsSI('Q', 'P', obj.st1_o.p.v, ...
#                    'H', h, obj.st1_o.fluid);
#                obj.st1_o.T = CoolProp.PropsSI('T', 'P', obj.st1_o.p.v, ...
#                    'Q', obj.st1_o.x, obj.st1_o.fluid);
#            else
#                obj.st1_o.T = CoolProp.PropsSI('T', 'P', obj.st1_o.p.v,'H', ...
#                    h, obj.st1_o.fluid);
#            end
#        end
#        function get_st2_i(obj)
#            % Calculate inlet properties of stream 2
#            obj.st2_i.fluid = obj.st2_o.fluid;
#            obj.st2_i.q_m = obj.st2_o.q_m;
#            obj.st2_i.p = obj.st2_o.p;
#            h = obj.st2_o.h - (obj.st1_i.h - obj.st1_o.h) ...
#                .* obj.st1_i.q_m.v ./ obj.st2_i.q_m.v;
#            h_l = CoolProp.PropsSI('H', 'P', obj.st2_i.p.v, 'Q', 0, obj.st2_i.fluid);
#            h_g = CoolProp.PropsSI('H', 'P', obj.st2_i.p.v, 'Q', 1, obj.st2_i.fluid);
#            if (h >= h_l && h <= h_g)
#                obj.st2_i.x = CoolProp.PropsSI('Q', 'P', obj.st2_i.p.v, ...
#                    'H', h, obj.st2_i.fluid);
#                obj.st2_i.T = CoolProp.PropsSI('T', 'P', obj.st2_i.p.v, ...
#                    'Q', obj.st2_i.x, obj.st2_i.fluid);
#            else
#                obj.st2_i.T = CoolProp.PropsSI('T', 'P', obj.st2_i.p.v,'H', ...
#                    h, obj.st2_i.fluid);
#            end
#        end
#        function get_imcprs_st2_i(obj)
#            % Calculate inlet properties of stream 2 (incompressible fluid)
#            obj.st2_i.fluid = obj.st2_o.fluid;
#            obj.st2_i.q_m = obj.st2_o.q_m;
#            obj.st2_i.p = obj.st2_o.p;
#            h = obj.st2_o.h - (obj.st1_i.h - obj.st1_o.h) ...
#                .* obj.st1_i.q_m.v ./ obj.st2_i.q_m.v;
#            if isempty(obj.st2_i.x)
#                obj.st2_i.T = CoolProp.PropsSI('T', 'P', obj.st2_i.p.v, ...
#                    'H', h, obj.st2_i.fluid);
#            end
#        end
#        function get_st2_o(obj)
#            % Calculate onlet properties of stream 2
#            obj.st2_o.fluid = obj.st2_i.fluid;
#            obj.st2_o.q_m = obj.st2_i.q_m;
#            obj.st2_o.p = obj.st2_i.p;
#            h = obj.st2_i.h + (obj.st1_i.h - obj.st1_o.h) ...
#                .* obj.st1_i.q_m.v ./ obj.st2_i.q_m.v;
#            h_l = CoolProp.PropsSI('H', 'P', obj.st2_o.p.v, 'Q', 0, obj.st2_o.fluid);
#            h_g = CoolProp.PropsSI('H', 'P', obj.st2_o.p.v, 'Q', 1, obj.st2_o.fluid);
#            if (h >= h_l && h <= h_g)
#                obj.st2_o.x = CoolProp.PropsSI('Q', 'P', obj.st2_o.p.v, ...
#                    'H', h, obj.st2_o.fluid);
#                obj.st2_o.T = CoolProp.PropsSI('T', 'P', obj.st2_o.p.v, ...
#                    'Q', obj.st2_o.x, obj.st2_o.fluid);
#            else
#                obj.st2_o.T = CoolProp.PropsSI('T', 'P', obj.st2_o.p.v, ...
#                    'H', h, obj.st2_o.fluid);
#            end
#        end
#        function get_imcprs_st2_o(obj)
#            % Calculate outlet properties of stream 2 (imcompressible fluid)
#            obj.st2_o.fluid = obj.st2_i.fluid;
#            obj.st2_o.q_m = obj.st2_i.q_m;
#            obj.st2_o.p = obj.st2_i.p;
#            h = obj.st2_i.h + (obj.st1_i.h - obj.st1_o.h) ...
#                .* obj.st1_i.q_m.v ./ obj.st2_i.q_m.v;
#            if isempty(obj.st2_o.x)
#                obj.st2_o.T = CoolProp.PropsSI('T', 'H', h, 'P', ...
#                    obj.st2_o.p.v, obj.st2_o.fluid);
#            end
#        end
#        function calcSt1_o(obj)
#            % Calculate outlet properties of stream 1
#            obj.st1_i.flowTo(obj.st1_o);
#            obj.st1_o.p = obj.st1_i.p;
#            if ~isempty(obj.st1_o.x)
#                obj.st1_o.T = CoolProp.PropsSI('T', 'P', obj.st1_o.p.v, ...
#                    'Q', obj.st1_o.x, obj.st1_o.fluid);
#            end
#        end
#        function get_q_m_2(obj)
#            % Calculate mass flow rate of stream 2
#            obj.st2_i.q_m.v = obj.st1_i.q_m.v .* (obj.st1_o.h - ...
#                obj.st1_i.h) ./ (obj.st2_i.h - obj.st2_o.h);
#        end
#    end
#    methods
#        function DeltaT = get.DeltaT(obj)
#            DeltaT(1) = abs(obj.st1_i.T - obj.st2_o.T);
#            DeltaT(2) = abs(obj.st2_i.T - obj.st1_o.T);
#        end
#    end

if __name__ == '__main__':
    he = HeatExchanger()
    he.st1_o.fluid = 'water'
    he.st1_o.T = 700
    he.st1_o.P = 1e5
    he.st1_o.dot_m[0] = 1

    he.st2_i.fluid = Const.FLUID[1]
    he.st2_i.T = 500
    he.st2_i.P = 1e5
    he.st2_i.dot_m[0] = 2

    he.st2_o.fluid = he.st2_i.fluid
    he.st2_o.T = 400
    he.st2_o.P = 1e5
    he.st2_o.dot_m[0] = 3

    he.calc_st1_i()
    he.calc_st1_o()
    he.calc_st2_i()
    he.calc_st2_o()

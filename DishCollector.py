"""DishCollector is a kind of Collector which uses dish mirror as the reflector
and uses volumetric receiver
"""
from Stream import Stream
from AirPipe import AirPipe
from InsLayer import InsLayer
from Ambient import Ambient
from CoolProp.CoolProp import PropsSI
import Const
from scipy.optimize import fsolve
import numpy as np


class DishCollector:
    gamma = 1       # Intercept factor of the collector
    rho = 0.8         # Reflectance of the collector
    shading = 1     # Shading factor of the collector
    d_ap = 0.25       # Aperture diameter of the dish receiver, m
    d_cav = 0.45       # Diameter of the cavity of the dish receiver, m
    dep_cav = 0.38     # Depth of the cavity of the dish receiver, m
    theta = np.deg2rad(45)   # Dish aperture angle(0 is horizontal,
    # pi/2 is vertically down), rad
    A = 23.28         # Aperture area of the collector, m^2

    def __init__(self):
        self.amb = Ambient()
        self.st_i = Stream()
        self.st_o = Stream()
        self.airPipe = AirPipe()
        self.insLayer = InsLayer()

    @property
    def q_use(self):
        return self.st_i.flow_rate[0] * (self.st_o.h - self.st_i.h)

    @property
    def q_tot(self):
        return self.amb.irradiance * self.A

    @property
    def eta(self):
        return self.q_use / self.q_tot

    @property
    def d_bar_cav(self):
        return self.d_cav - self.airPipe.d_i - 2 * self.airPipe.delta_a

    @property
    def A_ins(self):
        d_o = self.insLayer.d_i + 2 * self.insLayer.delta
        return np.pi * d_o * (self.dep_cav + self.insLayer.delta)

    @property
    def A_cav(self):
        return np.pi * self.d_bar_cav ** 2 / 4 + \
            np.pi * self.d_bar_cav * self.dep_cav + \
            np.pi * (self.d_bar_cav ** 2 - self.d_ap ** 2) / 4

    def q_in(self):
        # The accepted energy from the reflector, W
        return self.amb.irradiance * self.A * self.gamma * self.shading * self.rho

    def q_dr_1_1(self):
        # The accepted energy from the reflector, W
        h_o = PropsSI('H', 'T', self.st_o.temperature,
                      'P', self.st_o.pressure, self.st_o.fluid)
        h_i = PropsSI('H', 'T', self.st_i.temperature,
                      'P', self.st_i.pressure, self.st_i.fluid)
        return self.st_i.flow_rate[0] * (h_o - h_i)

    def q_dr_1_2(self):
        #  Heat transferred from the air pipe to the air, W
        average_temperature = (self.st_i.temperature + self.st_o.temperature)/2
        average_pressure = (self.st_i.pressure + self.st_o.pressure)/2
        density = PropsSI('D', 'T', average_temperature, 'P', average_pressure, self.st_i.fluid)
        v = 4 * self.st_i.flow_rate[0] / (np.pi * self.airPipe.d_i ** 2 * density)
        mu = PropsSI('V', 'T', average_temperature, 'P', average_pressure, self.st_i.fluid)
        re = density * v * self.airPipe.d_i / mu
        cp = PropsSI('C', 'T', average_temperature, 'P', average_pressure, self.st_i.fluid)
        k = PropsSI('L', 'T', average_temperature, 'P', average_pressure, self.st_i.fluid)
        pr = cp * mu / k
        mu_cav = PropsSI('V', 'T', self.airPipe.temperature, 'P', average_pressure, self.st_i.fluid)
        Nu_prime = Const.Nu_in_pipe(re, pr, mu, mu_cav)

        c_r = 1 + 3.5 * self.airPipe.d_i / (self.d_cav - self.airPipe.d_i
                                            - 2 * self.airPipe.delta_a)
        Nu = c_r * Nu_prime

        h = Nu * k / self.airPipe.d_i

        H_prime_c = self.airPipe.d_i + 2 * self.airPipe.delta_a
        N = np.floor(self.dep_cav / H_prime_c)
        H_c = self.dep_cav / N
        L_c = N * np.sqrt((np.pi * self.d_cav)**2 + H_c**2)
        A_airPipe = np.pi * self.airPipe.d_i * L_c

        DeltaT1 = self.airPipe.temperature - self.st_i.temperature
        DeltaT2 = self.airPipe.temperature - self.st_o.temperature
        DeltaT = Const.log_mean(DeltaT1, DeltaT2)

        return h * A_airPipe * DeltaT

    def q_ref(self):
        # Reflected energy by the receiver, W
        A_ap = np.pi * self.d_ap ** 2 / 4
        alpha_eff = self.airPipe.alpha / \
            (self.airPipe.alpha + (1 - self.airPipe.alpha) *
             (A_ap / self.A_cav))
        return self.q_in() * (1 - alpha_eff)

    def q_cond_conv(self):
        # Convection loss from the insulating layer, W
        mu = PropsSI('V', 'T', self.amb.temperature, 'P', self.amb.pressure, self.amb.fluid)
        density = PropsSI('D', 'T', self.amb.temperature, 'P',
                          self.amb.pressure, self.amb.fluid)
        nu = mu / density
        d_o = self.insLayer.d_i + 2 * self.insLayer.delta
        Re = self.amb.wind_speed * d_o / nu

        Cp = PropsSI('C', 'T', self.amb.temperature, 'P', self.amb.pressure, self.amb.fluid)
        k = PropsSI('L', 'T', self.amb.temperature, 'P', self.amb.pressure, self.amb.fluid)
        Pr = Cp * mu / k

        Nu = Const.Nu_of_external_cylinder(Re, Pr)

        h = Nu * k / d_o
        A_ins = self.A_ins
        return h * A_ins * (self.insLayer.temperature - self.amb.temperature)

    def q_cond_rad(self):
        return self.insLayer.epsilon * self.A_ins * \
                Const.SIGMA * (self.insLayer.temperature ** 4 - self.amb.temperature ** 4)

    def q_cond_tot(self):
        # Heat loss from air pipe to the insulating layer, W
        d_o = self.insLayer.d_i + 2 * self.insLayer.delta
        return (self.airPipe.temperature - self.insLayer.temperature) / \
            (np.log(d_o / self.insLayer.d_i) /
             (2 * np.pi * self.insLayer.lamb * self.dep_cav))

    def q_conv_tot(self):
        # Total convection loss, W
        average_temperature = (self.airPipe.temperature + self.amb.temperature) / 2
        # Film temperature is used
        k = PropsSI('L', 'T', average_temperature, 'P', self.amb.pressure, self.amb.fluid)

        beta = PropsSI('ISOBARIC_EXPANSION_COEFFICIENT',
                       'T', average_temperature, 'P', self.amb.pressure, self.amb.fluid)
        mu = PropsSI('V', 'T', average_temperature, 'P', self.amb.pressure, self.amb.fluid)
        density = PropsSI('D', 'T', average_temperature, 'P', self.amb.pressure, self.amb.fluid)
        nu = mu / density
        Gr = Const.G * beta * (self.airPipe.temperature - self.amb.temperature) * \
            self.d_bar_cav ** 3 / nu ** 2

        Nu = Const.Nu_nat_conv(Gr, self.airPipe.temperature, self.amb.temperature, self.theta,
                               self.d_ap, self.d_bar_cav)
        h_nat = k * Nu / self.d_bar_cav

        h_for = 0.1967 * self.amb.wind_speed ** 1.849

        return (h_nat + h_for) * self.A_cav * (self.airPipe.temperature - self.amb.temperature)

    def q_rad_emit(self):
        # Emitted radiation loss, W
        A_ap = np.pi * self.d_ap ** 2 / 4
        alpha_eff = self.airPipe.alpha / \
            (self.airPipe.alpha + (1 - self.airPipe.alpha) *
             (A_ap / self.A_cav))
        epsilon_cav = alpha_eff
        return epsilon_cav * A_ap * Const.SIGMA * \
            (self.airPipe.temperature ** 4 - self.amb.temperature ** 4)

    def CalcDishCollector1(self, x):
        # CalcDishCollector Use expressions to calculation parameters of dish
        # collector
        #   First expression expresses q_dr_1 in two different forms
        #   Second expression expresses q_cond_tot = q_cond_conv + q_cond_rad
        #   Third expression expresses q_in = q_ref + q_dr_1 + q_cond_tot +
        #   q_conv_tot + q_rad_emit
        self.airPipe.temperature = x[0]
        self.insLayer.temperature = x[1]
        self.st_i.flow_rate[0] = x[2]
        # F = cell(3,1)
        # F{1} = dc.q_dr_1_1 - dc.q_dr_1_2
        # F{2} = dc.q_cond_tot - dc.q_cond_conv - dc.q_cond_rad
        # F{3} = dc.q_dr_1_1 + dc.q_ref + (dc.q_cond_tot ...
        #                 + dc.q_conv_tot + dc.q_rad_emit) - dc.q_in
        return np.array([self.q_dr_1_1() - self.q_dr_1_2(),
                        self.q_cond_tot() - self.q_cond_conv() - self.q_cond_rad(),
                        self.q_dr_1_1() + self.q_ref() +
                        (self.q_cond_tot() + self.q_conv_tot() + self.q_rad_emit())
                        - self.q_in()])

    def get_dot_m(self):
        # Known inlet and outlet temperature to calculate the flow rate
        self.st_o.fluid = self.st_i.fluid
        self.st_o.flow_rate = self.st_i.flow_rate
        # Assume no pressure loss
        self.st_o.pressure = self.st_i.pressure
        self.st_o.pressure = self.st_i.pressure
        guess = np.array([500, 300, 0.1])
        # options = optimset('Display','iter')
        fsolve(self.CalcDishCollector1, guess)

    def CalcDishCollector2(self, x):
        # CalcDishCollector Use expressions to calculation parameters of dish
        # collector
        #   First expression expresses q_dr_1 in two different forms
        #   Second expression expresses q_cond_tot = q_cond_conv + q_cond_rad
        #   Third expression expresses q_in = q_ref + q_dr_1 + q_cond_tot +
        #   q_conv_tot + q_rad_emit
        self.airPipe.temperature = x[0]
        self.insLayer.temperature = x[1]
        self.st_o.temperature = x[2]
        #      F = cell(3,1)
        #      F{1} = self gc.q_dr_1_1 - dc.q_dr_1_2
        #      F{2} = self gc.q_cond_tot - dc.q_cond_conv - dc.q_cond_rad
        #      F{3} = self gc.q_dr_1_1 + dc.q_ref + (dc.q_cond_tot ...
        #          + self gc.q_conv_tot + dc.q_rad_emit) - dc.q_in
        return np.array([self.q_dr_1_1() - self.q_dr_1_2(),
                        self.q_cond_tot() - self.q_cond_conv() - self.q_cond_rad(),
                        self.q_dr_1_1() + self.q_ref() +
                         (self.q_cond_tot() + self.q_conv_tot() +
                         self.q_rad_emit()) - self.q_in()])

    def get_T_o(self):
        # Known inlet temperature and flow rate to calculate outlet
        # temperature
        self.st_o.fluid = self.st_i.fluid
        self.st_o.flow_rate = self.st_i.flow_rate
        # Assume no pressure loss
        self.st_o.pressure = self.st_i.pressure
        self.st_o.pressure = self.st_i.pressure
        guess = np.array([1500, 400, 1000])
        # options = optimset('Display','iter')
        fsolve(self.CalcDishCollector2, guess)

    def CalcDishCollector3(self, x):
        # CalcDishCollector Use expressions to calculation parameters of dish
        # collector
        #   First expression expresses q_dr_1 in two different forms
        #   Second expression expresses q_cond_tot = q_cond_conv + q_cond_rad
        #   Third expression expresses q_in = q_ref + q_dr_1 + q_cond_tot +
        #   q_conv_tot + q_rad_emit
        self.airPipe.temperature = x[0]
        self.insLayer.temperature = x[1]
        self.A = x[2]
        #     F = cell(3,1)
        #     F{1} = self.q_dr_1_1 - self.q_dr_1_2
        #     F{2} = self.q_cond_tot - self.q_cond_conv - self.q_cond_rad
        #     F{3} = self.q_dr_1_1 + self.q_ref + (self.q_cond_tot ...
        #         + self.q_conv_tot + self.q_rad_emit) - self.q_in
        return np.array([self.q_dr_1_1() - self.q_dr_1_2(),
                        self.q_cond_tot() - self.q_cond_conv() - self.q_cond_rad(),
                        self.q_dr_1_1() + self.q_ref() + (self.q_cond_tot() +
                                                          self.q_conv_tot() +
                                                          self.q_rad_emit())
                        - self.q_in()])

    def get_A(self):
        self.st_o.fluid = self.st_i.fluid
        self.st_o.flow_rate = self.st_i.flow_rate
        # Assume no pressure loss
        self.st_o.pressure = self.st_i.pressure
        self.st_o.pressure = self.st_i.pressure
        guess = np.array([500, 300, 19])
        # options = optimset('Display','iter')
        x = fsolve(self.CalcDishCollector3, guess)
        self.A = x[2]


if __name__ == '__main__':
    dc = DishCollector()
    st_i = Stream()
    st_i.fluid = Const.FLUID[2]
    st_i.temperature = Const.convert_temperature(150, 'C', 'K')
    st_i.pressure = 4e5
    # st_i.flow_rate[0] = 0.07
    dc.st_i = st_i
    st_o = Stream()
    st_o.fluid = Const.FLUID[2]
    st_o.temperature = Const.convert_temperature(239.26, 'C', 'K')
    st_o.pressure = 4e5
    dc.st_o = st_o
    dc.amb.irradiance = 700
    dc.get_dot_m()

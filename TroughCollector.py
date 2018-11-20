"""This class defines a kind of Collector who uses trough as the reflector
and uses vacumn receiver
"""
from Ambient import Ambient
from Stream import Stream
from CoolProp import CoolProp
import Const
from math import radians, log, pi


class TroughCollector:
    def __init__(self, A=545, w=5.76, v_min=1.1, v_max=2.9):
        self.A = A
        self.w = w
        self.v_min = v_min
        self.v_max = v_max
        self.rho = 0.94     # Reflectance of the collector
        self.shading = 1    # Shading factor of the collector
        self.tau = 0.95     # Transmissivity of trough receiver
        self.alpha = 0.96   # Absorptivity of the absorber selective
# coating of trough collector
        self.Fe = 0.97      # Soiling factor of the trough collector
        self.d_i = 0.066    # Inner diameter of the absorber, m
        self.d_o = 0.07     # Outer diameter of the absorber, m
        self.phi = radians(70)  # Incidence angle, rad
        self.f = 0          # Focal length, m
        self.len = 0        # Length of the collector, m
        self.tc_type = None  # type of the collector
        self.gamma = 0.93   # Intercept factor of the collector
        self.n_in_a_row = 0
        self.st_i = Stream()
        self.st_i.fluid = Const.FLUID[3]
        self.st_o = Stream()
        self.st_o.fluid = Const.FLUID[3]
        self.amb = Ambient()
        self.v = 0          # Actual average oil speed in the trough collector
        # Dependent properties

    @property
    def U(self):
        # This function is used to calculate the overall heat transfer
        # coefficient of trough receiver with the fluid average
        # temperature of T.
        T = (self.st_i.T + self.st_o.T) / 2
        if T < 473.15:
            return 0.687257 + 0.001941 * (T - self.amb.T) + \
                0.000026 * (T - self.amb.T) ** 2
        elif T > 573.15:
            return 2.895474 - 0.0164 * (T - self.amb.T) + \
                0.000065 * (T - self.amb.T) ** 2
        else:
            return 1.433242 - 0.00566 * (T - self.amb.T) + \
                0.000046 * (T - self.amb.T) ** 2

    @property
    def K(self):
        # Used to calculate the incidence angle coefficient
        return 1 - 2.23073e-4 * self.phi - 1.1e-4 * self.phi ** 2 \
            + 3.18596e-6 * self.phi ** 3 - 4.85509e-8 * self.phi ** 4

    @property
    def L_per_q_m(self):
        # Required length of unit mass flow rate of the collector to
        # heat the temperature of the working fluid from
        # st_i.T upto st_o.T
        para = pi * self.d_o
        eta_opt_0 = self.rho * self.gamma * self.tau * self.alpha
        q = self.amb.I * self.w * eta_opt_0 * self.K * self.Fe / para
        T = (self.st_i.T + self.st_o.T) / 2
        P = (self.st_i.P + self.st_o.P) / 2
        cp = CoolProp.PropsSI('C', 'T', T, 'P', P, self.st_i.fluid)
        U = self.U
        DeltaT_o = self.st_o.T - (self.amb.T + q / U)
        DeltaT_i = self.st_i.T - (self.amb.T + q / U)
        return - cp * log(DeltaT_o / DeltaT_i) / (U * para)

    @property
    def calculate(self):
        # Calculate the number of trough collectors required and the
        # actual speed in the pipe
        self.n = 0
        self.v = self.n * self.v_s
        while self.v < self.v_min:
            self.n = self.n + 1
            self.v = self.n * self.v_s
        if self.v > self.v_max:
            raise RuntimeError('No proper speed found!')
        else:
            self.st_i.dot_m = self.n * self.q_use / (self.st_o.h - self.st_i.h)
            self.st_o.dot_m = self.st_i.dot_m
            # L = self.L_per_q_m * self.st_i.dot_m
            # self.n = L / (self.A / self.w)

    @property
    def q_use(self):
            return self.q_tot * self.eta

    @property
    def q_tot(self):
        return self.amb.I * self.A

    @property
    def eta(self):
        eta = (self.st_o.h - self.st_i.h) / \
             (self.amb.I * self.w * self.L_per_q_m)
        return eta

    @property
    def v_s(self):
        fluid = self.st_i.fluid
        T = (self.st_i.T + self.st_o.T) / 2
        P = (self.st_i.P + self.st_o.P) / 2
        density = CoolProp.PropsSI('D', 'T', T, 'P', P, fluid)
        q_m_basic = self.q_use / (self.st_o.h - self.st_i.h)
        return 4 * q_m_basic / (density * pi * self.d_i ** 2)


if __name__ == '__main__':
    tc = TroughCollector()
    tc.st_i.T = 400
    tc.st_i.P = 2e6
    tc.st_o.T = 500
    tc.st_o.P = 2e6

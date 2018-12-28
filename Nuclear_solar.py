from Stream import Stream
import numpy as np
from CoolProp.CoolProp import PropsSI as ps
import matplotlib.pyplot as plt

T_i = 500   #  初温，˚C
p_c = 4000  # 排气压力，Pa
mass_flow_rate = 61.3  # 主汽流量，kg/s

st_i = Stream()
st_i.temperature_celcius = T_i
st_i.flow_rate = mass_flow_rate

st_o = Stream()
st_o.pressure = p_c

st_c = Stream()
st_c.pressure = p_c
st_c.quality = 0

number = 40    # number组数据，压力从p0增加到p1
p0 = 10e6
p1 = 80e6
p = np.linspace(p0, p1, number)
T0 = 400
T1 = 850
Delta_T = 50
T = range(T0, T1, Delta_T)
for j in T:
    st_i.temperature_celcius = j
    efficiency_ideal = []
    for i in range(number):
        st_i.pressure = p[i]
        st_o.quality = ps('Q', 'P', st_o.pressure, 'S', st_i.s, 'water')
        efficiency_ideal.append((st_i.h - st_o.h) / (st_i.h - st_c.h))
        # print('P = {P:.3e}, eta = {eta:.3f}'.format(P=p[i], eta=efficiency_ideal))
    plt.plot(p, efficiency_ideal, label = '$T_0$='+str(j)+'˚C')
plt.legend()
plt.xlabel("Turbine inlet pressure ($p_0$), Pa")
plt.ylabel("Ideal efficiency of Rankine cycle ($\eta_i$)")
plt.title("$p_c$ = 4000 Pa")
plt.show()

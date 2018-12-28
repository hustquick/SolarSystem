from Stream import Stream
import numpy as np
from CoolProp.CoolProp import PropsSI as ps
import matplotlib.pyplot as plt

st = Stream()

T0 = 100
T1 = 600
Delta_T = 50

P0 = 1e5
P1 = 1e8
P_num = 1000
P = np.linspace(P0, P1, P_num)

for T in range(T0, T1, Delta_T):
    st.temperature_celcius = T
    enthalpy = []
    for i in range(P_num):
        st.pressure = P[i]
        enthalpy.append(st.h)
    plt.plot(enthalpy, P, label='$T$='+str(T)+'˚C')
h0 = []
h1 = []
num = 1000
P_s = ps('P_CRITICAL', 'water')
p = np.linspace(P0, P_s, num)
for i in range(num):
    h0.append(ps('H','Q', 0, 'P', p[i], 'water'))
    h1.append(ps('H','Q', 1, 'P', p[i], 'water'))
plt.plot(h0, p, '--', color='red')
plt.plot(h1, p, '--', color='red')
plt.legend(loc=1)
plt.ylabel("Pressure, Pa")
plt.xlabel("Enthalpy, J/kg")
plt.title('Water P-h diagram')
plt.show()

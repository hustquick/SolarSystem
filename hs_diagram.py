from Stream import Stream
import numpy as np
from CoolProp.CoolProp import PropsSI as ps
import matplotlib.pyplot as plt

st = Stream()

T0 = 100
T1 = 600
Delta_T = 50

s0 = 1e5
s1 = 1e8
s_num = 1000
S = np.linspace(s0, s1, s_num)

for T in range(T0, T1, Delta_T):
    st.temperature_celcius = T
    enthalpy = []
    for i in range(s_num):
        st.pressure = ps('P', 'S', S[i], 'T', st.temperature, 'water')
        enthalpy.append(st.h)
    plt.plot(S, enthalpy, label='$T$='+str(T)+'˚C')
h0 = []
h1 = []
num = 1000
S_s =
p = np.linspace(P0, P_s, num)
for i in range(num):
    h0.append(ps('H','Q', 0, 'P', p[i], 'water'))
    h1.append(ps('H','Q', 1, 'P', p[i], 'water'))
plt.plot(p, h0, '--', color = 'red')
plt.plot(p, h1, '--', color = 'red')
plt.legend(loc=1)
plt.xlabel("Pressure, Pa")
plt.ylabel("Enthalpy, J/kg")
plt.title('Water P-h diagram')
plt.show()

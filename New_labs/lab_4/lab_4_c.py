import math
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
def func1(y, t):
    p, p1 = y
    dydt = [p1, math.cos(t)-2*p1-3*p]
    return dydt
def func2(y, t):
    p, p1 = y
    dydt =[p1, 1*(1-p**2)*p1-p]
    return dydt

ti = np.arange(0, 2*math.pi, 0.1)
y0 = [0, 0]
sol = odeint(func1, y0, ti)
plt.plot(ti, sol [:,0] ,"r",label="y")
plt.plot(ti, sol[:,1],"g",label="y'")
plt.xlabel("t",fontsize =17)
plt.ylabel("y",fontsize =17)
plt.grid ()
plt.legend ()
#plt.savefig("Fig3.1.png")
plt.show ()


ti = np.arange(0, 30, 0.1)
y0 = [2,0]
sol = odeint(func2, y0, ti)
plt.plot(ti, sol [:,0] ,"r",label="z")
plt.plot(ti, sol[:,1],"g",label="z'")
plt.xlabel("t",fontsize =17)
plt.ylabel("y",fontsize =17)
plt.grid ()
plt.legend ()
#plt.savefig("Fig3.2.png")
plt.show ()
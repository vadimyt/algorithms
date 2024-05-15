from scipy. integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def func1(y,t):
    return y**2-y*t
def func2(y,t):
    return y**2+1
y0=0.1
ti=np.arange (0,1,0.1)
yi=odeint (func1,y0,ti)
print (yi)
# График функции у(t)
plt.plot(ti,yi,"o-r",alpha=0.7,lw=5, mec="g",mew=2,ms=10) 
plt.xlabel("t,время",fontsize=20)
plt.ylabel("y",fontsize=20)
plt.tick_params(axis="both",labelsize=15) 
plt.grid (True)
#plt.savefig("Fig1.1.png")
plt.show()

y0=0.1
ti=np.arange (0,1,0.1)
yi=odeint (func2,y0,ti)
print (yi)
# График функции у(t)
plt.plot(ti,yi,"o-r",alpha=0.7,lw=5,mec="r",mew=2,ms=10) 
plt.xlabel("t,время",fontsize=20)
plt.ylabel("y",fontsize=20)
plt.tick_params(axis="both",labelsize=15) 
plt.grid (True)
#plt.savefig("Fig1.2.png")
plt.show()
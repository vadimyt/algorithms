from scipy. integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def func2(eq,t):
    a=0.2
    b=0.2
    c=5
    x,y,z=eq
    return [-y-z,x+a*z,b+z*(x-c)]
a=-8/3; b=-10; c=28
ti=np.arange (0,100,0.01)
y0=[1,1,1]
sol=odeint(func2,y0,ti)
x=sol [:,0]; y=sol [:,1]; z=sol[:,2]
plt.subplot(221) # две строки, два столбца, 1-й рисунок
plt.plot(x,y,lw=1)
plt.title (" Фазовый портрет")
plt.xlabel("x")
plt.ylabel("y")
plt.grid ()
plt.tight_layout()
plt.subplot(221) # две строки,
plt.plot(x,y,lw=1)
plt.title(" Фазовый портрет")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.tight_layout ()
plt.subplot(222) # две строки, два столбца, 2-й рисунок
plt.plot (ti, x,lw=1, color="orange")
plt.title("x(t)")
plt.xlabel("t")
plt.ylabel("x")
plt.grid(); plt.tight_layout()
plt.subplot(223) # две строки, два столбца, 3-й рисунок
plt.plot(ti,y,lw=1,color="g")
plt.title ("y(t)")
plt.xlabel ("t")
plt.ylabel("y")
plt.grid()
plt.tight_layout()
plt.subplot (224) # две строки, два столбца, 4-й рисунок
plt.plot(ti,z,lw=1,color="r")
plt.title("z(t)")
plt.xlabel("t")
plt.ylabel("z")
plt.grid()
plt.tight_layout()
#plt.savefig("Fig2.png")
plt. show ()
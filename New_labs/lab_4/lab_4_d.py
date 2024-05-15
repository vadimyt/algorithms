from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def func8(eq, t):
    x, y = eq
    return [r1*x - l1*x*y, l2*x*y - b2*y]

r1=0.5; l1=0.01; l2=0.01; b2=0.2; g1=0.0005
ti=np.arange(0, 1000, 0.1)
y0 = [25, 5]
sol1 = odeint(func8, y0, ti)
x = sol1[:, 0]
y = sol1[:, 1]

plt.subplot(121)
plt.plot(ti, x, "r", label="x")
plt.plot(ti, y, "b", label="y")
plt.xlabel("t", fontsize=17)
plt.ylabel("x,y", fontsize=17)
plt.grid(); plt.legend()
plt.title("a)")

plt.subplot(122)
plt.plot(x, y, color="g")
plt.xlabel("x", fontsize=17)
plt.ylabel("y", fontsize=17)
plt.grid()
plt.title("b)")
plt.tight_layout()
#plt.savefig("figg4.png")
plt.show()

def func9(eq1, t):
    x1, y1 = eq1
    return [r1*x1 - l1*x1*y1 - g1*x1**2, l2*x1*y1 - b2*y1]

sol2 = odeint(func9, y0, ti)
x = sol2[:, 0]
y = sol2[:, 1]

plt.subplot(121)
plt.plot(ti, x, "r", label="x", lw=1)
plt.plot(ti, y, "b", label="y", lw=1)
plt.xlabel("t", fontsize=17)
plt.ylabel("x,y", fontsize=17)
plt.grid()
plt.legend()
plt.title("a)")
plt.subplot(122)
plt.plot(x, y, color="g", lw=1)
plt.xlabel("x", fontsize=17)
plt.ylabel("y", fontsize=17)
plt.grid()
plt.title("b)")
plt.tight_layout()
#plt.savefig("figg4.2.png")
plt.show()
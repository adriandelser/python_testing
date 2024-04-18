import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm



class Source:
    def __init__(self,m) -> None:
        self.m = m
        self.coords = (0,0)

    def u(self,location):
        x,y = np.array(location) - np.array(self.coords)
        velocityU = (self.m/2*np.pi) * x/(x**2 + y**2)
        return velocityU
    def v(self,location):
        x,y = np.array(location) - np.array(self.coords)
        velocityU = (self.m/2*np.pi) * y/(x**2 + y**2)
        return velocityU
    @np.vectorize
    def phi(self,location):
        x,y = np.array(location)# - np.array(self.coords)
        r = np.sqrt(x**2 + y**2)
        phi = self.m/np.pi *np.log(r)
        return phi
    
mysource = Source(m=1)


m=np.pi
lim = 5
delta = 0.025
x = np.arange(-lim, lim, delta)
y = np.arange(-lim, lim, delta)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
Z0 = (m/np.pi )*np.log(R)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

fig, ax = plt.subplots()
CS = ax.contour(X, Y, Z0)
ax.clabel(CS, inline=True, fontsize=10)
ax.set_title('Simplest default with labels')
plt.show()
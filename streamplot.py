#%%
import numpy as np
import matplotlib.pyplot as plt

Y, X = np.mgrid[-3:3:100j, -3:3:100j]
U = -1 - X**2 + Y
V = 1 + X - Y**2
speed = np.sqrt(U**2 + V**2)

fig, ax = plt.subplots()
ax.streamplot(X, Y, U, V, color='r')

plt.show()

# %%
nm 
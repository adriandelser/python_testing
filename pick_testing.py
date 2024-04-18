import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Create a new figure and axes instance
fig, ax = plt.subplots()

ax.plot(np.random.rand(100), 'o', picker=5)  # 5 points tolerance

p = Polygon([[0,0],[1,0],[1,1]])
ax.add_patch(p)

def on_pick(event):
    line = event.artist
    xdata, ydata = line.get_data()
    ind = event.ind[0]
    print(ind)
    print(f'on pick line: {xdata[ind]:.3f}, {ydata[ind]:.3f}')

cid = fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()
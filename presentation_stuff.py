import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_drone(ax, x, y, color):
    drone = patches.Rectangle((x-0.02, y-0.02), 0.04, 0.04, linewidth=1, edgecolor=color, facecolor=color)
    ax.add_patch(drone)

def plot_curved_arrow(ax, x1, y1, x2, y2, color):
    style = "Simple,tail_width=0.05,head_width=0.2,head_length=0.2"
    kw = dict(arrowstyle=style, color=color)
    a = patches.FancyArrowPatch((x1, y1), (x2, y2), connectionstyle="arc3,rad=.5", **kw)
    ax.add_patch(a)

fig, ax = plt.subplots()

# Set axis limits and hide axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Plot drones
plot_drone(ax, 0.2, 0.2, 'red')
plot_drone(ax, 0.8, 0.8, 'blue')

# Plot paths with curved arrows
plot_curved_arrow(ax, 0.2, 0.2, 0.7, 0.6, 'red')
plot_curved_arrow(ax, 0.8, 0.8, 0.3, 0.4, 'blue')

# Add text
plt.text(0.15, 0.12, 'Drone A', color='red', fontsize=12)
plt.text(0.75, 0.72, 'Drone B', color='blue', fontsize=12)
plt.text(0.4, 0.6, 'Deconflicted Paths', color='green', fontsize=12)

# Show plot
plt.title('Drone Deconfliction')
plt.show()

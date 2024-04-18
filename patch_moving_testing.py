import numpy as np
import matplotlib.pyplot as plt

class ArrowDragger:
    def __init__(self, arrow):
        self.arrow = arrow
        self.press = None
        self.ax = arrow.axes

        self.cidpress = self.arrow.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.arrow.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.arrow.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.arrow.axes: return

        contains, attrd = self.arrow.contains(event)
        if not contains: return
        
        x0, y0 = self.arrow.xy1  # Get starting position
        self.press = (x0, y0, event.xdata, event.ydata)

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.arrow.axes: return
        
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        
        # Adjusting the positions of the arrow
        self.arrow.set_positions((x0 + dx, y0 + dy), self.arrow.xy2)
        
        self.arrow.figure.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.arrow.figure.canvas.draw()

    def disconnect(self):
        self.arrow.figure.canvas.mpl_disconnect(self.cidpress)
        self.arrow.figure.canvas.mpl_disconnect(self.cidrelease)
        self.arrow.figure.canvas.mpl_disconnect(self.cidmotion)


# Test the ArrowDragger
fig, ax = plt.subplots()

arrow = ax.arrow(0.2, 0.2, 0.5, 0.5, head_width=0.05, head_length=0.1, fc='blue', ec='black')
dragger = ArrowDragger(arrow)

plt.show()

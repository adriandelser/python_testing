from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# vertices = [[0,0],[0,1],[1,1],[1,0]]

vertices = np.array([[[-1.98387097,  0.02419355]],
                     [[ 2.01612903,  0.00806452]],
                     [[-0.00806452,  2.00806452]]])

vertices = vertices.squeeze(axis=1)

point = [1.012,1]

poly0 = Polygon(vertices, closed=True, fill=True, color=(1,0,0, 1)) # False
poly1 = Polygon(vertices, closed=True, fill=True, color='r')        # False
poly2 = Polygon(vertices, closed=True, fill=True, color=(1,0,0,0))  # True
poly3 = Polygon(vertices, fill = False, alpha = 0)                  # True
poly4 = Polygon(vertices, fill = False)                             # False                       
poly5 = Polygon(vertices)                                           # True                       

poly6 = Polygon(
                np.array(vertices),  # x,y coordinates of the vertices
                edgecolor=(0,0,0,1),      # Set border color to Black (R,G,B,A) where A is transparency
                facecolor=(0,0,1,0.5),     # set fill color to blue and alpha to 0.5
                # alpha=0.5,             # make it semi-transparent, applies to whole patch 
                closed=True,
                linewidth=2.0 
            )


for idx, poly in enumerate((poly0, poly1, poly2, poly3, poly4, poly5,poly6)):
    print(f"Polygon {idx} contains point {point}: {poly.contains_point(point, radius=0)}")


# Create a figure and axis for plotting
fig, ax = plt.subplots()

# Add the polygons to the axis
ax.add_patch(poly5)

# plt.show()

print(matplotlib.get_backend())
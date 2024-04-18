from shapely.geometry import Polygon
from shapely import intersection
import matplotlib.pyplot as plt


# Example polygons (replace these with your actual polygons)
polygon1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
polygon2 = Polygon([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)])

# Check if the two polygons overlap
for i in range(10000):
    a = intersection(polygon1,polygon2)

overlap = polygon1.intersects(polygon2)


print("Do the polygons overlap?", overlap)


fix, ax = plt.subplots()
print(polygon1.exterior.xy)
#add polygons to plot
ax.add_patch(plt.Polygon(polygon1.exterior, color='red'))

plt.show()
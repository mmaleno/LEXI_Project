import matplotlib.pyplot as plt

image_name = 'thePark.png'

im = plt.imread(image_name)
implot = plt.imshow(im)
#plt.ylim(200,400)
#plt.xlim(100,300)

# put a blue dot at (10, 20)
plt.scatter([10], [20])

# put a red dot, size 40, at 2 locations:
plt.scatter(x=[30, 40], y=[50, 60], c='r', s=40)

plt.show()
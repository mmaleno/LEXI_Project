# live plot script - 6/14/18
# it works!!!!!! at 12:31am on 6/15
# just need to document a bit more and clean it up to get it on the pi

# No longer updated - last updated on 6/25/18 (to let it run on Mac)
# Last real update was 6/24/18
# When running this on the pi, be sure to uncomment PyQt5, win, mng

from urllib.request import urlopen
#from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

image_name = 'thePark.png'        # be sure screenshot of map is .png
dataURL = 'http://192.168.0.5'   # 'http://192.168.0.12/'   # IP of ESP8266 on 715E7C
fig = plt.figure()
im = np.flipud(plt.imread(image_name))  # need to flip image up/down
                                        # due to how pixels are indexed
imHeight, imWidth, channels = im.shape  # detect image size, ignore channels

zeroLong = -117.754903
zeroLat = 33.652619

imWidthLong = -117.753419
imHeightLat = 33.653867

# function to grab data from ESP8266's website/IP
def readData():

    print("Start readData")
    page = urlopen(dataURL)  # unpack webpage contents
    xVal = 0
    yVal = 0

    # cycle thru page to find what we are looking for
    for line in page:

        # in this case, we used 'x: ' to find the line with x data
        # we need " b' " in front of the string to turn it into a byte-type
        if b'x: ' in line:

            # find start and end indices of x value
            start_index = line.decode('utf-8').find(' ')
            end_index = line.decode('utf-8').find('<')

            # create a string from the extracted byte-value
            xValStr = line[start_index+1:end_index].decode('utf-8')
            print("Grabbed x Coord: " + xValStr)

            # convert extracted value into usable form
            xVal = float(xValStr)

        if b'y: ' in line:
            start_index = line.decode('utf-8').find(' ')
            end_index = line.decode('utf-8').find('<')
            yValStr = line[start_index+1:end_index].decode('utf-8')
            print("Grabbed y Coord: " + yValStr)
            yVal = float(yValStr)
            break

    page.close()                # close python's reading of URL
    valArray = [xVal,yVal]      # pack extracted values into array
    print("End readData")
    return valArray

# initialize our plot so animation looks clean
def initPlot():
    plt.clf()           # clear plot
    plt.axis('off')    # remove axes from plot
    plt.ylim(0,imHeight)     # force y axis to start at 0 at bottom left
    plt.xlim(0,imWidth)     # force x axis to start at 0 at bottom left
    implot = plt.imshow(im) # print our map behind the data
    plt.title('Lexi\'s Current Location', fontsize=24)    # print a fitting title to our figure ADD APOSTROPHE

def convertCoord(valArray):
    xDeg = valArray[0]
    yDeg = valArray[1]
    print("xDeg: " + str(xDeg))
    print("yDeg: " + str(yDeg))
    xPix = (imWidth / (imWidthLong - zeroLong)) * (xDeg - zeroLong)
    yPix = (imHeight / (imHeightLat - zeroLat)) * (yDeg - zeroLat)
    return [xPix, yPix]

def animate(i):
    print("Start animate")
    initPlot()
    #try:
    #    win = fig.canvas.manager.window
    #except AttributeError:
    #    win = fig.canvas.window()
    #toolbar = win.findChild(QtWidgets.QToolBar)
    #toolbar.setVisible(False)
    valArray = readData()
    print("valArray[0]: " + str(valArray[0]))
    print("valArray[1]: " + str(valArray[1]))
    coordPix = convertCoord(valArray)
    print("Long: " + str(valArray[0]))
    print("Lat:  " + str(valArray[1]))
    print("xPix: " + str(coordPix[0]))
    print("yPix: " + str(coordPix[1]))
    plt.scatter([coordPix[0]], [coordPix[1]], c='r', s=100)
    print("End animate")

#mng = plt.get_current_fig_manager()
#mng.window.showMaximized()

ani = animation.FuncAnimation(fig, animate)

plt.show()

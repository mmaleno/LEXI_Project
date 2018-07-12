# helperLEXI.py - 7/8/18
# a clean version of live_animate.py (alongside mainLEXI.py)

# see mainLEXI.py for TODO

# When running this on the pi, be sure to uncomment PyQt5, win, and mng

version = 'mac'     # set this equal to 'pi' when running on pi

from urllib.request import urlopen                  # for reading data from ESP8266
if (version == 'pi'):
    from PyQt5 import QtWidgets                        # for controlling GUI window on pi
import matplotlib.pyplot as plt                     # for plotting on GUI window
import matplotlib.animation as animation            # for live-animating GUI window
from matplotlib.font_manager import FontProperties  # for changing font in GUI window
import numpy as np                                  # for plotting on GUI window
import time                                         # for forcing the program to slow down
import os                                           # for pinging our ESP8266

fig = plt.figure()              # create a figure within our plot
fontReg = FontProperties()      # create a font object for regular weight
fontReg.set_weight('normal')    # set the regular font object's weight to normal
fontBold = FontProperties()     # create a font object for bold weight
fontBold.set_weight('bold')     # set the bold font object's weight to bold
fontBold.set_size(24)           # set the bold font object's size to a title-size

image_name = 'thePark.png'        # be sure screenshot of map is .png
hostname = '192.168.0.5'          # version of IP for ping
dataURL = 'http://192.168.0.5'    # IP of ESP8266 for urlopen

im = np.flipud(plt.imread(image_name))  # need to flip image up/down...
                                        # ...due to how pixels are indexed
imHeight, imWidth, channels = im.shape  # detect image size, ignore channels

# set the (0,0) GPS coordinates on the map image (bottom left of image)
zeroLong = -117.754903
zeroLat = 33.652619

# set the (xMax, yMax) GPS coordinates on the map image (top right of image)
imWidthLong = -117.753419
imHeightLat = 33.653867

# function to see if tracker is connected
def checkWifiConnectivity():
    wifiConnected = 0 # by default, we say our ESP8266 is not connected. We're pessimistic!

    response = os.system("ping -c 1 " + hostname) # ping our ESP8266
    
    # check response
    if (response == 0):
        print(hostname, 'is up!')
        wifiConnected = 1           # set wifiConnected to TRUE
    else:
        print(hostname, 'is down!') # print error message, leave wifiConnected as FALSE

    return wifiConnected

# function to grab data from ESP8266's website/IP
def readData():

    print("Start readData")

    wifiConnected = checkWifiConnectivity() # boolean confirmation that we are...
                                            # ...connected to tracker via wifi
    
    if (wifiConnected): # wifiConnected is 1 is it is connected

        # initialize coordinates as 0
        xVal = 0
        yVal = 0

        page = urlopen(dataURL)  # unpack webpage contents

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

            if b'fix: ' in line:
                start_index = line.decode('utf-8').find(' ')
                end_index = line.decode('utf-8').find('<')
                fixStatusStr = line[start_index+1:end_index].decode('utf-8')
                print("Fix Status: " + fixStatusStr)
                fixStatus = int(fixStatusStr)
                break

        page.close()                # close python's reading of URL

        valArray = [xVal,yVal, wifiConnected, fixStatus]      # pack important info into array

        print("End readData")
        return valArray
        
    else:   # if we make it to this block, then wifiConnected == 0 and tracker is offline

        print("urlRead FAILED!!")
        return [0,0,wifiConnected]

# initialize our plot so animation looks clean
def initPlot():
    plt.clf()                # clear plot
    plt.axis('off')          # remove axes from plot
    plt.ylim(0,imHeight)     # force y axis to start at 0 at bottom left
    plt.xlim(0,imWidth)      # force x axis to start at 0 at bottom left
    implot = plt.imshow(im)  # print our map behind the data
    
    # enlarge the map to fill (almost) the entire vertical, and shift
    # it to the right to make room for other text
    plt.subplots_adjust(left=0.43, bottom=0.01, top=0.99)
    
    # remove toolbar from window to make it cleaner
    # only works on pi due to Qt5 backend
    if (version == 'pi'):
        try:
            win = fig.canvas.manager.window
        except AttributeError:
            win = fig.canvas.window()
        toolbar = win.findChild(QtWidgets.QToolBar)
        toolbar.setVisible(False)
    
    # give our window a fitting title
    fig.canvas.set_window_title('LEXI Tracker')
    
# convert GPS coordinates into plottable (x,y) coordinates
def convertCoord(valArray):

    # unpack valArray values into (more) usable variables
    xDeg = valArray[0]
    yDeg = valArray[1]

    # print the extracted values for convenient console debugging
    print("xDeg: " + str(xDeg))
    print("yDeg: " + str(yDeg))

    # formula for converting the GPS coordinates into plottable pixel coordinates
    xPix = (imWidth / (imWidthLong - zeroLong)) * (xDeg - zeroLong)
    yPix = (imHeight / (imHeightLat - zeroLat)) * (yDeg - zeroLat)

    return [xPix, yPix]

# animation loop to display live coordinates on figure window
def animate(i):
    print("Start animate")

    stringWifiConnected = ''
    stringFixStatus = ''
    
    
    # extract GPS data (see readData() in this file above)
    valArray = readData()

    # print the extracted values for convenient console debugging
    print("valArray[0]: " + str(valArray[0]))
    print("valArray[1]: " + str(valArray[1]))

    # convert extracted GPS values into coordinates (see convertCoord above)
    coordPix = convertCoord(valArray)
    
    # print the extracted and converted values for debugging
    print("Long: " + str(valArray[0]))
    print("Lat:  " + str(valArray[1]))
    print("xPix: " + str(coordPix[0]))
    print("yPix: " + str(coordPix[1]))

    initPlot()    # see initPlot() in this file above

    # Determine string of wifi status
    if (valArray[2]):
        stringWifiConnected = 'Is'
        # Determine string of GPS status
        if (valArray[3]):
            stringFixStatus = 'Has Fix'
        else:
            stringFixStatus = 'No Fix'
    else:
        stringWifiConnected = 'Not'
        stringFixStatus = 'Pending Tracker Connection'

      

    # print relevant information off to the left hand side of our window (see values ~0.02)
    plt.text(0.05, 0.8, 'Lexi\'s Current \n    Location', fontproperties=fontBold,transform=plt.gcf().transFigure)
    plt.text(0.02, 0.7, 'Tracker: ' + stringWifiConnected + ' Connected', fontsize=18, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.6, 'GPS: ' + stringFixStatus, fontsize=18, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.45, 'Last Successful\n Transmission:    ' + '4:00' + ' PM', fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.35, 'Lat: ' + str(valArray[1]) + ' N', fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.17, 0.35, 'Long: ' + str(valArray[0]) + ' W', fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.28, 'Speed: ' + '100' + ' mph', fontsize=14, transform=plt.gcf().transFigure)

    # plot a red dot of the position on the map
    # scatter takes (xCoord, yCoord, dotColor, dotSize)
    plt.scatter([coordPix[0]], [coordPix[1]], c='r', s=100)

    print("End animate")

# animate the figure so that it is getting live GPS updates
def update():
    if (version == 'pi'):
        # Maximize the size of the window so that it takes up the whole display
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
    
    # loop once plt.show() runs
    ani = animation.FuncAnimation(fig, animate)
    
    # load the plot with its settings into the window. It will now run animate
    plt.show()
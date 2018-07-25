# helperLEXI.py - 7/24/18
# a clean version of live_animate.py (alongside mainLEXI.py)

# see mainLEXI.py for TODO

# Quick trick to detect what operating system we are on,
# so that OS-specific lines are included automatically
import platform
version = ''                        # should be 'pi' when running on pi, mac if otherwise

if (platform.system() == 'Linux'):
    version = 'pi'
else:
    version = 'mac'

from urllib.request import urlopen                  # for reading data from ESP8266
if (version == 'pi'):
    from PyQt5 import QtWidgets                        # for controlling GUI window on pi
import matplotlib.pyplot as plt                     # for plotting on GUI window
import matplotlib.animation as animation            # for live-animating GUI window
from matplotlib.font_manager import FontProperties  # for changing font in GUI window
import numpy as np                                  # for plotting on GUI window
import time                                         # for forcing the program to slow down
import os                                           # for pinging our ESP8266
import signal                                       # for making a timeout for readData()

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

lastSuccessHour = 0
lastSuccessMinute = 0
lastSuccessSecond = 0
lastSuccessMeridian = 'NEVER'


# function to see if tracker is connected
def checkWifiConnectivity():
    wifiConnected = 0 # by default, we say our ESP8266 is not connected. We're pessimistic!

    response = os.system("ping -c 1 -t 4 " + hostname)   # ping our ESP8266
                                                        # -c 1 means one packet
                                                        # -t 4 means 4-second timeout
    
    # check response
    if (response == 0):
        print(hostname, 'is up!')
        wifiConnected = 1           # set wifiConnected to TRUE
    else:
        print(hostname, 'is down!') # print error message, leave wifiConnected as FALSE

    return wifiConnected


# function needed for readData timeout functionality
def handler(signum, frame):
    print("readData timer is up!")
    raise


# returns a word to describe the RSSI value (lay-person friendly)
def convertRSSItoWord(rssi):
    if (rssi > -30):
        return "Very Good"
    elif (rssi > -40):
        return "Good"
    elif (rssi > -50):
        return "Average"
    elif (rssi > -60):
        return "Below Average"
    elif (rssi > -70):
        return "Weak"
    elif (rssi > -80):
        return "Very Weak"
    elif (rssi >-90):
        return "Minimal"
    else:
        return "Not Connected"


# function to grab data from ESP8266's website/IP
def readData():

    print("Start readData")

    global lastSuccessHour
    global lastSuccessMinute    
    global lastSuccessSecond    
    global lastSuccessMeridian

    reachedSats = 0

    wifiConnected = checkWifiConnectivity() # boolean confirmation that we are...
                                            # ...connected to tracker via wifi
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(3)

    #if(readDataBool):
    if (wifiConnected): # wifiConnected is 1 is it is connected

        # initialize coordinates as 0
        xVal = 0
        yVal = 0
        numSats = 0
        print("Right before urlopen")
        try:
            page = urlopen(dataURL)  # unpack webpage contents
        except:
            signal.alarm(0)
            print("urlRead FAILED!!")
            return [0,0,wifiConnected, 0, 0, lastSuccessHour, lastSuccessMinute, lastSuccessSecond, lastSuccessMeridian, -90]
        print("right after urlopen")

        # cycle thru page to find what we are looking for
        for line in page:

            if b'wifi: ' in line:
                start_index = line.decode('utf-8').find(' ')
                end_index = line.decode('utf-8').find('<')
                rssiStr = line[start_index+1:end_index].decode('utf-8')
                print("Wifi Strength: " + rssiStr)
                rssi = int(rssiStr)
            
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

            if b'fix?: ' in line:
                start_index = line.decode('utf-8').find(' ')
                end_index = line.decode('utf-8').find('<')
                fixStatusStr = line[start_index+1:end_index].decode('utf-8')
                print("Fix Status: " + fixStatusStr)
                fixStatus = int(fixStatusStr)
            
            if b'sats: ' in line:
                start_index = line.decode('utf-8').find(' ')
                end_index = line.decode('utf-8').find('<')
                numSatsStr = line[start_index+1:end_index].decode('utf-8')
                print("# of Sats: " + numSatsStr)
                numSats = int(numSatsStr)
                reachedSats = 1
            
            if(reachedSats):
                if (fixStatus):
                    for line in page:
                        if b'hour: ' in line:
                            start_index = line.decode('utf-8').find(' ')
                            end_index = line.decode('utf-8').find('<')
                            hourStr = line[start_index+1:end_index].decode('utf-8')
                            print("Hour: " + hourStr)
                            hour = int(hourStr)
                    
                        if b'min: ' in line:
                            start_index = line.decode('utf-8').find(' ')
                            end_index = line.decode('utf-8').find('<')
                            minStr = line[start_index+1:end_index].decode('utf-8')
                            print("Minute: " + minStr)
                            minute = int(minStr)
                    
                        if b'sec: ' in line:
                            start_index = line.decode('utf-8').find(' ')
                            end_index = line.decode('utf-8').find('<')
                            secStr = line[start_index+1:end_index].decode('utf-8')
                            print("Second: " + secStr)
                            second = int(secStr)
                    
                        if b'mer: ' in line:
                            start_index = line.decode('utf-8').find(' ')
                            end_index = line.decode('utf-8').find('<')
                            merStr = line[start_index+1:end_index].decode('utf-8')
                            print("Meridian: " + merStr)
                            mer = merStr
                            break
                else:
                    hour = lastSuccessHour
                    minute = lastSuccessMinute
                    second = lastSuccessSecond
                    mer = lastSuccessMeridian
                    break



        page.close()                # close python's reading of URL

        valArray = [xVal,yVal, wifiConnected, fixStatus, numSats, hour, minute, second, mer, rssi]     # pack important info into array
        lastSuccessHour = hour
        lastSuccessMinute = minute
        lastSuccessSecond = second
        lastSuccessMeridian = mer

        print("End readData")
        return valArray        

    else:   # if we make it to this block, then wifiConnected == 0 and tracker is offline
        signal.alarm(0)
        print("urlRead FAILED!!")
        return [0,0,wifiConnected, 0, 0, lastSuccessHour, lastSuccessMinute, lastSuccessSecond, lastSuccessMeridian, -90]

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
    print("valArray[2]: " + str(valArray[2]))
    print("valArray[3]: " + str(valArray[3]))
    print("valArray[4]: " + str(valArray[4]))
    print("valArray[5]: " + str(valArray[5]))
    print("valArray[6]: " + str(valArray[6]))
    print("valArray[7]: " + str(valArray[7]))
    print("valArray[8]: " + str(valArray[8]))
    print("valArray[8]: " + str(valArray[9]))

    # convert extracted GPS values into coordinates (see convertCoord above)
    coordPix = convertCoord(valArray)
    
    # print the extracted and converted values for debugging
    print("Long: " + str(valArray[0]))
    print("Lat:  " + str(valArray[1]))
    print("xPix: " + str(coordPix[0]))
    print("yPix: " + str(coordPix[1]))

    initPlot()    # see initPlot() in this file above

    stringWiFiStrength = convertRSSItoWord(valArray[9])

    # Determine string of wifi status
    if (valArray[2]):
        stringWifiConnected = 'Is'
        # Determine string of GPS status
        if (valArray[3]):
            stringFixStatus = str(valArray[4]) + ' Sats Connected'
        else:
            stringFixStatus = 'No Fix'
            valArray[0] = 0
            valArray[1] = 0
    else:
        stringWifiConnected = 'Not'
        stringFixStatus = 'Waiting for Tracker'

    stringHour = str(valArray[5])
    stringMinute = str(valArray[6])
    stringSecond = str(valArray[7])
    stringMeridian = valArray[8]
    
    if (valArray[5]<10):
        stringHour = "0" + str(valArray[5])
    if (valArray[6]<10):
        stringMinute = "0" + str(valArray[6])
    if (valArray[7]<10):
        stringSecond = "0" + str(valArray[7])

    stringTime = stringHour + ":" + stringMinute + ":" + stringSecond + " " + stringMeridian

    # fix stringTime to be just "NEVER" if there has never been a successful transmission
    if (stringTime == "00:00:00 NEVER"):
        stringTime = "Never"

    print()
    # print relevant information off to the left hand side of our window (see values ~0.02)
    plt.text(0.05, 0.8, 'Lexi\'s Current \n    Location', fontproperties=fontBold,transform=plt.gcf().transFigure)
    plt.text(0.02, 0.7, 'Tracker: ' + stringWifiConnected + ' Connected', fontsize=18, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.6, 'GPS: ' + stringFixStatus, fontsize=18, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.45, 'Last Successful\n Transmission:   ' + stringTime, fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.35, 'Tracker Strength: ' + stringWiFiStrength, fontsize=14, transform=plt.gcf().transFigure)
    if (valArray[2]):
        plt.text(0.24, 0.3, '(' + str(valArray[9]) + ' dBm)', fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.25, 'Lat: ' + str(valArray[1]) + ' N', fontsize=14, transform=plt.gcf().transFigure)
    plt.text(0.02, 0.19, 'Long: ' + str(-valArray[0]) + ' W', fontsize=14, transform=plt.gcf().transFigure)
    #plt.text(0.02, 0.222, 'Speed: ' + '100' + ' mph', fontsize=14, transform=plt.gcf().transFigure)

    # plot a red dot of the position on the map
    # scatter takes (xCoord, yCoord, dotColor, dotSize)
    plt.scatter([coordPix[0]], [coordPix[1]], c='r', s=100)

    print("End animate")
    time.sleep(1)

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
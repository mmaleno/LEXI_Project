# classes.py
# A file to contain the classes that are used in the lexi project
# experiemental - purely an experiement to make the code cleaner as
# of 7/11/18

class Figure:

    fontReg = ''
    fontBold = ''
    satImage = ''       # need to make this an Image object
    hostname = ''
    dataURL = ''
    im = ''
    # need imHeight, imWidth, channels = im.shape somewhere
    zeroLong = ''
    zeroLat = ''
    imWidthLong = ''
    imHeightLat = ''

    class Image:
        image_name = ''

    class Telemetry:
        
        stringWifiConnected = ''
        stringFixStatus = ''
        xDeg = ''
        yDeg = ''
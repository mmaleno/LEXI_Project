# 06/12/18 - first shot at webpage-grabbing script
#   /13/   - value filtering, value extraction

# need to write a bash script to re-run this script
# if it runs for more than 5 seconds (also need to
# write aruduino to reboot ESP8266 if no good)

# need to get nice python web and graphing capabilities
import urllib.request
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


image_name = 'thePark.png'

im = plt.imread(image_name)

#plt.show(block=False)

while(1):
	


	# create a variable to pack out webpage contents into
	page = urllib.request.urlopen('http://192.168.0.11/')

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
			print(xValStr)

			# bring extracted value back to its 'raw' form
			xVal = int(xValStr)

		if b'y: ' in line:
			start_index = line.decode('utf-8').find(' ')
			end_index = line.decode('utf-8').find('<')
			yValStr = line[start_index+1:end_index].decode('utf-8')
			print(yValStr)
			yVal = int(yValStr)
			break
	page.close()

	print('Plot point')
	# put a blue dot at (10, 20)
	plt.scatter([xVal], [yVal])

	# put a red dot, size 40, at 2 locations:
	#plt.scatter(x=[30, 40], y=[50, 60], c='r', s=40)
	implot = plt.imshow(im)
	pyplot.draw()
	start = time.time()
	print('Start delay')
	time.sleep(10)
	print('End delay')
	
	#plt.close()

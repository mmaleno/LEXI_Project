# mainLEXI.py - 7/27/18
# As of 7/25 1:45am, there are no known bugs!! It appears error handling is smooth

# TODO:  -display text of "real word" location (ex: "driveway", "backyard", etc.)
#        -display battery voltage - need some resistors from home to make voltage divider
#        -Display last known battery, if last known battery <20% then say probably dead
#        -add auto script run (without having to tap terminal)
#        -add last known coordinates to display last location of Lexi, and make dot other color
#        -change color of text when not connected
#        -ENABLE REMOTE TALKING TO LEXI?????? (need mic and speaker)
#        -Add multiple-dog functionality
#       Allow multiple files by passing fig object as argument in function
#       Add easy turn on - need to add switch/button to RUN pins onboard the pi
#       Change map to be image of home, update lat/long calculation variables for home
#       Calibrate good/average/weak wifi RSSI values for home property

from helperLEXI import update

# animate the figure so that it is getting live GPS updates
update()

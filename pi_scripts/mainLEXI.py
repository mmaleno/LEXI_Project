# mainLEXI.py - 7/24/18
# a clean version of live_animate.py (alongside helperLEXI.py)

# TODO:  -remove copious print statements (maybe not, they've been helpful)
#        -display text of "real word" location (ex: "driveway", "backyard", etc.)
#        -give readData() a timeout, because if tracker disconnects during readData()
#         then system gets hung up
#        -make system compare current time to last successful transmission time,
#         if it is more than 10-15 seconds, then have tracker disconnected
#        -display battery voltage - need some resistors from home to make voltage divider
#        -ENABLE REMOTE TALKING TO LEXI?????? (need mic and speaker)
#        -Add multiple-dog functionality (lowest priority)
#       Allow multiple files by passing fig object as argument in function (like FDIR)
#       Add auto-startup - need to add switch/button to RUN pins onboard the pi
#       Change map to be image of home, update lat/long calculation variables for home
#       Calibrate good/average/weak wifi RSSI values for home property

from helperLEXI import update

# animate the figure so that it is getting live GPS updates
update()

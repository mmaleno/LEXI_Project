# mainLEXI.py - 6/25/18
# a clean version of live_animate.py (alongside helperLEXI.py)

# TODO:  -remove copious print statements (maybe not, they've been helpful)
#        -display text of "real word" location (ex: "driveway", "backyard", etc.),
#        -put tracker connection pending text on next line (have text wrap)
#        -make system compare current time to last successful transmission time,
#         if it is more than 10-15 seconds, then have tracker disconnected
#        -Instead of 00:00:00 NEVER, make just "NEVER"
#        -prevent pi from turning off screen after idle time (IMPORTANT)
#        -display wifi signal strength of tracker
#        -display battery voltage
#        -ENABLE REMOTE TALKING TO LEXI?????? (need mic and speaker)
#        -Add multiple-dog functionality (lowest priority)
#       Allow multiple files by passing fig object as argument in function (like FDIR)
#       Add auto-startup - need to add switch/button to RUN pins onboard the pi

from helperLEXI import update

# animate the figure so that it is getting live GPS updates
update()

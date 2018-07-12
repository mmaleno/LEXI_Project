# mainLEXI.py - 6/25/18
# a clean version of live_animate.py (alongside helperLEXI.py)

# TODO:  -remove copious print statements (maybe not, they've been helpful)
#        -display text of "real word" location (ex: "driveway", "backyard", etc.),
#        -put tracker connection pending text on next line (have text wrap)
#        -display wifi signal strength of tracker
#        -display battery voltage
#        -ENABLE REMOTE TALKING TO LEXI?????? (need mic and speaker)
#       Allow multiple files by passing fig object as argument in function (like FDIR)
#       Add auto-startup - need to add switch/button to RUN pins onboard the pi

from helperLEXI import update

# animate the figure so that it is getting live GPS updates
update()

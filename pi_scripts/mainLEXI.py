# mainLEXI.py - 6/25/18
# a clean version of live_animate.py (alongside helperLEXI.py)

# TODO: implement connected/disconnected status, remove copious print statements
#       display time of last plotted position, display text of
#       "real word" location (ex: "driveway", "backyard", etc.),
#       display gps status (connected, # of sats, lat/long, sped), display wifi
#       status (connected, signal strength)

from helperLEXI import update

# animate the figure so that it is getting live GPS updates
update()

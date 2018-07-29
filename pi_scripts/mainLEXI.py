#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: mainLEXI.py

Author: Max Maleno

Last Updated: 7/28/18

"""

# TODO:
#        -add last known coordinates to display last location of Lexi, and make dot other color
#        -ENABLE REMOTE TALKING TO LEXI?????? (need mic and speaker)
#        -Add multiple-dog functionality
#       Add easy turn on - need to add switch/button to RUN pins onboard the pi
#       Change map to be image of home, update lat/long calculation variables for home
#       Calibrate good/average/weak wifi RSSI values for home property
#       Try to install on Alex's computer so I can give directions on running program

from helperLEXI import update

# animate the figure so that it is getting live GPS updates
update()

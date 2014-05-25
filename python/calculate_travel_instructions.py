# -*- coding: utf-8 -*-
"""
Created on Sun May 25 14:12:12 2014

@author: rustenburg
"""

import tools
from systems import nyc


subway,lines,stations,trains = nyc()

tools.travel_instructions(subway,lines,order=["transfers","stops","distance"], cutoff = 70)
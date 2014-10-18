#!/usr/bin/env python

import time
import os

def log(s):
	print str(time.time()) + ": " + s
	
def say(s):
	os.system('flite -voice kalit -t ' + s + '&')
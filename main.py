#!/user/bin/env python

import time
from datetime import datetime
from random import randint
import json
from urllib.request import urlopen
import colorsys
from sys import exit
import threading
import numpy as np
import math
import blinkt

global address
global ads_percentage_today
global status
global glu_relative_days, glu_relative_hours, glu_relative_minutes
global response
global bright
global startTime
global endTime

address = "http://pihole/admin/api.php?"
fallOff = 1.9
scanSpeed = 4
blinktON = 0.04
blinktOFF = 0.0
sTime = time.time()
startTime = datetime.strptime('22:00:00', "%H:%M:%S")
endTime = datetime.strptime('7:59:59', "%H:%M:%S")


blinkt.set_clear_on_exit()

def getJsonData():
	with urlopen(address) as response:
		pihole = response.read()
		response = (json.loads(pihole))
	return response

def setPecentage(ads_percentage, r, g, b):
	percentage = ads_percentage/100
	percentage *= blinkt.NUM_PIXELS

	for x in range(blinkt.NUM_PIXELS):
		if percentage < 0:
			r, g, b = 0, 0, 0
		else:
			r, g, b = [int(min(percentage, 1.0) * c) for c in [r, g, b]]
			blinkt.set_pixel(x, r, g, b)
			percentage -= 1

			blinkt.set_brightness(getBrightness())
			blinkt.show()

def notEnabled(fwhm):
	x = np.arange(0, blinkt.NUM_PIXELS, 1, float)
	y = x[:, np.newaxis]
	x0, y0 = 3.5, 3.5
	fwhm = fwhm
	gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
	return gauss

def getBrightness():
	today = datetime.now()
	time = today.time()

	if time >= startTime.time() or time <= endTime.time():
		#print("Blinkt is OFF")
		return blinktOFF
	else:
		#print("Blinkt is ON")
		return blinktON

def clearBlinkt():
	blinkt.clear()
	blinkt.show()

def main():
	clearBlinkt()

	response = getJsonData()
	status = response['status']

	try:
		while (status == "enabled"):
			response = getJsonData()

			ads_percentage_today = response['ads_percentage_today']
			glu_relative_days = response['gravity_last_updated']['relative']['days']
			glu_relative_hours = response['gravity_last_updated']['relative']['hours']
			glu_relative_minutes = response['gravity_last_updated']['relative']['minutes']
			status = response['status']

			#print("Pi-Hole: %s Days, %s Hours, %s Minutes \nAds Percentage: %s" % (glu_relative_days, glu_relative_hours, glu_relative_minutes, ads_percentage_today))
			setPecentage(ads_percentage_today, 0, 225, 0)

		while (status != "enabled"):
			response = getJsonData()
			status = response['status']

			delta = (time.time() - sTime)
			offset = (math.sin(delta * scanSpeed) + 1) / 2
			hue = int(round(offset * 360))
			max_val = blinkt.NUM_PIXELS - 1
			offset = int(round(offset * max_val))

			for x in range(blinkt.NUM_PIXELS):
				sat = 1.0

				val = max_val - (abs(offset - x) * fallOff)
				val /= float(max_val)
				val = max(val, 0.0)

				xhue = hue
				xhue += (1 - val) * 10
				xhue %= 360
				xhue /= 360.0

				r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(xhue, sat, val)]

				blinkt.set_pixel(x, r, g, b, val / 4)

			blinkt.set_brightness(blinktON)
			blinkt.show()

			time.sleep(0.001)

		main()

	except:
		clearBlinkt()

		eTime = time.time() + 90
		while time.time() < eTime:
			for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
				fwhm = 5.0 / z
				gauss = notEnabled(fwhm)
				start = time.time()
				y = 4

				for x in range(blinkt.NUM_PIXELS):
					h = 1.0
					s = 1.0
					v = gauss[x, y]
					rgb = colorsys.hsv_to_rgb(h, s, v)
					r, g, b = [int(255.0 * i) for i in rgb]
					blinkt.set_pixel(x, r, g, b)

				blinkt.set_brightness(blinktON)
				blinkt.show()
				end = time.time()
				t = end - start

				if t < 0.04:
					time.sleep(0.04 - t)

		main()

main()



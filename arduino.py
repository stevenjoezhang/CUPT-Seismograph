# -*- coding=utf-8 -*-
import serial
import re
import psutil as p
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import time

ser = serial.Serial("/dev/tty.usbmodem1421", 9600) # Replace tty.usbmodem1411 with your serial port
print(ser.isOpen())

POINTS = 1000
dataY = [None] * POINTS

fig, ax = plt.subplots()

ax.set_ylim([500, 1000])
ax.set_xlim([0, POINTS])
ax.set_autoscale_on(False)

ax.set_xticks([])
ax.set_yticks(range(500, 1001, 100))
ax.grid(True)

l_dataY, = ax.plot(range(POINTS), dataY, label = "Voltage (mv)")

ax.legend(loc = "upper center", ncol = 4, prop = font_manager.FontProperties(size = 10))

def getData():
	line = ser.readline()
	ser.flushInput()
	data = re.sub("\D", "", str(line))
	if (data != ""):
		num = int(data)
		return num

	return 0

def onTimer(ax):
	global dataY
	tmp = getData()
	if tmp == 0:
		return

	dataY = dataY[1:] + [tmp]
	l_dataY.set_ydata(dataY)
	ax.draw_artist(l_dataY)
	ax.figure.canvas.draw()
	string = str(tmp) + " " + str(time.time() - 1526030000);
	print(string)
	with open("data.txt", "a") as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
		f.write(string + "\n")

timer = fig.canvas.new_timer(interval = 10)
timer.add_callback(onTimer, ax)
timer.start()
plt.show()

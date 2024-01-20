import mysql.connector

import string
import psutil
import cpuinfo
#import smbus
#import time
import subprocess
import os


from time import sleep
from gpiozero import CPUTemperature, LoadAverage

mydb = mysql.connector.connect(
	host="localhost",
	user="machine_status",
	password="machine_status",
	database="machine_status"
)

while True:
	## Based on https://stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python
	cpufreq = psutil.cpu_freq()
	net_io = psutil.net_io_counters()
	partitions = psutil.disk_partitions()

	# Disk Information
	# get all disk partitions
	partitions = psutil.disk_partitions()
	for partition in partitions:
		if partition.mountpoint == '/':
			try:
				partition_usage = psutil.disk_usage(partition.mountpoint)
			except PermissionError:
				# this can be catched due to the disk that isn't ready
				continue

	cpu = CPUTemperature()
	la = LoadAverage()

	process = os.popen('cat /proc/loadavg | awk \'{print $1}\'')
	cmdread = process.read()
	process.close()
	cpu_usage = float(cmdread)
	number_of_logical_processors = psutil.cpu_count(logical=True)

	# Load percentage is load number [e.g.  0.44] divided by CPU count [RaspPi 5 = 4] times 100.
	load_ave = float( ( cpu_usage / number_of_logical_processors )* 100 )
	check_load_ave = int(float(load_ave))

	mycursor = mydb.cursor()
	sql = (
		"INSERT INTO current_status(cpuTemp, cpuPercent, diskFree, loadPercent )"
		"VALUES (%s, %s, %s, %s)"
	)
	val = (cpu.temperature, psutil.cpu_percent(), partition_usage.free, load_ave)

	mycursor.execute(sql, val)

	mydb.commit()
	sleep(10)

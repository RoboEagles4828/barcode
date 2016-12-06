#!/usr/bin/python3

import datetime

output_format = ".csv"
sum_extension = "-sum"

#get YYYY-MM-DD string
def get_date():
	return datetime.date.strftime(datetime.datetime.today().date(),"%Y-%m-%d")

#get HH-MM-SS string
def get_time():
	return datetime.time.strftime(datetime.datetime.now().time(), "%H:%M:%S")

#get number of seconds from time string
def time_to_seconds(time):
	t = time.split(":")
	return 3600 * int(t[0]) + 60 * int(t[1]) + int(t[2])

#get time string from number of seconds
def seconds_to_time(s):
	hr = int(s / 3600)
	s -= hr * 3600
	mn = int(s / 60)
	s -= mn * 60
	return str(hr) + ":" + str(mn) + ":" + str(s)

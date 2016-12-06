#!/usr/bin/python3

from record.date import *

#holds the name, and sign in times for 1 person
class Individual():
	def __init__(self, ID, name):
		self.ID = ID
		self.name = name
		self.times = []
		self.is_signed_in = False
		self.showed_up = False

	#print individual
	def __repr__(self):
		s = ""

		#don't print data if the person never showed up
		if self.showed_up:
			#name and ID
			s += self.name + " (" + str(self.ID) + ")\n"

			#print total time signed in
			s += "  " + self.combined_time() + "\n  "

			#print all time-stamps
			for time in self.times:
				s += time + " "

			#if signed in print current time stamp
			if self.is_signed_in:
				s += get_time()
			s += "\n"

		return s

	#sign individual in at current system time
	def sign_in(self):
		self.times.append(get_time())
		self.is_signed_in = not self.is_signed_in
		self.showed_up = True

	#net time present
	def combined_time(self):
		l = len(self.times)
		total_time = 0
		#add time difference between pairs of time stamps
		for i in range(int((l - int(self.is_signed_in)) / 2)):
			total_time += time_to_seconds(self.times[2*i + 1])
			total_time -= time_to_seconds(self.times[2*i])

		#if signed in than get time difference up to now
		if self.is_signed_in:
			total_time += time_to_seconds(get_time())
			total_time -= time_to_seconds(self.times[-1])

		return seconds_to_time(total_time)

	#JSON representation of individual
	def toJSON(self):		
		s = '"' + str(self.ID) + '":{'
		s += '"name":"' + self.name + '",'
		s += '"times":{'
		s += '"total":"' + self.combined_time() + '",'
		s += '"stamps":["'
		s += '","'.join(self.times)
		s += '"]}}'
		return s

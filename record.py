#!/usr/bin/python3

import os
import csv
import datetime

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

#holds the name, and sign in times for 1 person
class Individual():
	def __init__(self, ID, name):
		self.ID = ID
		self.name = name
		self.times = []
		self.is_signed_in = False
		self.showed_up = False

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

	#print individual
	def print(self):
		#don't print data if the person never showed up
		if self.showed_up:
			#print name and ID
			print(self.name + " (" + str(self.ID) + ")\t", end = "")

			#print total time signed in
			print(self.combined_time())

			#print all time-stamps
			for time in self.times:
				print(time + " ", end = "")

			#if signed in print current time stamp
			if self.is_signed_in:
				print(get_time(), end = "")
			
			print()


#holds all attendance data for each individual
class Record():
	def __init__(self, roster_file, attendance_folder, remember_old):
		self.remember_old = remember_old
		self.roster_file = roster_file
		self.attendance_file = attendance_folder + "/" + get_date()
		self.output_format = ".csv"
		self.build_record()

	#parse roster file into record of individuals
	def build_record(self):
		roster_data = open(self.roster_file, "r")
		self.record = {}
		for identity in csv.reader(roster_data, delimiter = ","):
			self.record[int(identity[0])] = Individual(int(identity[0]), identity[1])
		roster_data.close()

		#reload old attendance data from same day if specified
		if self.remember_old and os.path.exists(self.attendance_file + self.output_format):
			attendance_data = open(self.attendance_file + self.output_format, "r")
			for identity in csv.reader(attendance_data, delimiter = ","):
				try:
					ID = int(identity[0])
					l = len(identity)
					#make sure the old data's IDs matches roster and is valid
					if identity[1] == self.record[ID].name and l % 2 == 0 and l > 2:
						self.record[ID].times = identity[2:]
						self.record[ID].showed_up = True
					else:
						print("warning: name did not match ID ", end = "")
						print("could not parse " + identity[0] + "," + identity[1] + " ...")
				except:
					print("warning: could not parse " + identity[0] + "," + identity[1] + " ...")

	#get individual with specified ID
	def get_individual(self, ID):
		if ID in self.record:
			return self.record[ID]
		return None

	#find ID from name in the record
	def find_ID(self, name):
		for ID in self.record:
			if name == self.record[ID].name:
				return ID
		return None

	#sign-in individual with specified ID
	def sign_in(self, ID):
		self.record[ID].sign_in()

	#print record
	def print(self):
		for ID in self.record:
			self.record[ID].print()

	#write out record to attendence csv
	def write(self):
		file_time_stamps = self.attendance_file + self.output_format
		file_combined_time = self.attendance_file + "-sum" + self.output_format

		f1 = open(file_time_stamps, "w")
		f2 = open(file_combined_time, "w")

		writer1 = csv.writer(f1, delimiter = ",")
		writer2 = csv.writer(f2, delimiter = ",")

		for ID in self.record:
			individual = self.record[ID]
			#don't save data if the person never showed up
			if individual.showed_up:
				#lines to append to file
				row1 = [ID, individual.name]
				row2 = row1 + [individual.combined_time()]
				row1 += individual.times

				#sign out people who havent already
				if individual.is_signed_in:
					row1.append(get_time())
					print("Signed out " + individual.name + " (" + str(ID) + ")")

				#append time-stamps to file 1and combined time to file 2
				writer1.writerow(row1)
				writer2.writerow(row2)

		#flush buffer and close the files
		f1.flush()
		f1.close()
		
		f2.flush()
		f2.close()

	#track attendance and returns False if user quits
	def track_attendance(self):
		try:
			#prompt for ID
			inp = input("Enter ID: ")
			if len(inp) > 9:
				inp = inp[1:-1]
			ID = int(inp)

			#quit if negative number
			if ID < 0:
				return False

			if ID in self.record:
				#get individual with specified ID
				individual = self.record[ID]
				individual.sign_in()

				#display if individual signed in or out
				if individual.is_signed_in:
					print("Signed in ", end = "")
				else:
					print("Signed out ", end = "")

				#display individual's name and ID
				print(individual.name + " (" + str(ID) + ")")

			else:
				#no individuals with specified ID
				print("error: '" + str(ID) + "' in not a valid id number")
		except:
			#quit if 'q' or 'quit' or 'exit' typed in
			if inp == "q" or inp == "quit" or inp == "exit":
				return False

			#input is not an integer
			print("error: '" + inp + "' is not a number")

		return True

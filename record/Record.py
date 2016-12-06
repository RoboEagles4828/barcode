#!/usr/bin/python3

import csv
import os
from record.date import *
from record.Individual import Individual

#holds all attendance data for each individual
class Record():
	def __init__(self, roster_file, attendance_folder, remember_old, date=get_date()):
		self.remember_old = remember_old
		self.roster_file = roster_file
		self.date = date
		self.attendance_file = os.path.join(attendance_folder, date)
		self.build_record()

	#parse roster file into record of individuals
	def build_record(self):
		roster_data = open(self.roster_file, "r")
		self.record = {}
		for identity in csv.reader(roster_data, delimiter = ","):
			self.record[int(identity[0])] = Individual(int(identity[0]), identity[1])
		roster_data.close()

		#reload old attendance data from same day if specified
		if self.remember_old and os.path.exists(self.attendance_file + output_format):
			attendance_data = open(self.attendance_file + output_format, "r")
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
		file_time_stamps = self.attendance_file + output_format
		file_combined_time = self.attendance_file + sum_extension + output_format

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

	#JSON representation for record
	def toJSON(self):
		s = '"' + self.date + '":'

		#array of JSONs for each individual
		data = "{"
		for ID in self.record:
			individual = self.record[ID]
			if individual.showed_up:
				data += individual.toJSON()
				data += ","
		data = data[:-1] + "}"

		#if no people in record, return empty array
		if len(data) < 3:
			return s + "{}"
		return s + data

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

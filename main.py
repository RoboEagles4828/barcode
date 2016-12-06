#!/usr/bin/python3

import os
import record

attendance_folder = "attendance"
roster_file = "roster.csv"

#create attendance directory if not already made
if not os.path.exists(attendance_folder):
	os.makedirs(attendance_folder)

#whether to load old data from csv
remember_old = True
r = record.Record(roster_file, attendance_folder, remember_old)

#track attendance until user quits
while(True):
	if not r.track_attendance():
		print("Quitting...")
		break

print()
print(r)
r.write()

#!/usr/bin/python3

import os
import record

attendance_folder = "attendance"
roster_file = "roster.csv"

#returns True if the csv file doesn't end in "-sum" and is a ".csv"
def valid_attendance_file(f):
	of = record.output_format
	return not record.sum_extension in f and f[-len(of):] == of

#create attendance directory if not already made
if not os.path.exists(attendance_folder):
	os.makedirs(attendance_folder)

#get list of attendance ".csv" files that don't end in "-sum.csv"
files = [f.replace(record.output_format, "") for f in os.listdir(attendance_folder) if valid_attendance_file(f)]
files.sort()

#append json for each file to final json
json = '{'
for file in files:
	json += record.Record(roster_file, attendance_folder, True, file).toJSON()
	json += ","
json = json[:-1] + "}"

if len(json) < 2:
	json = ""
print(json)

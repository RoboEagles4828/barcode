import csv
import datetime

time = []
name = []

def idtoname(roster_file, num):
    file = open(roster_file, "r")
    csvfile = csv.reader(file, delimiter=",")
    for line in csvfile:
        if int(line[0]) == num:
            return True, line[1]
    return False, str(num)


def getid(roster_file):
    print "--- STARTING ID FETCH ---"
    filename = "attendance/attendance" + str(
        datetime.date.strftime(datetime.datetime.today().date(), "%m-%d-%y")) + ".csv"
    print "Log Name: " + filename

    idfile = open(filename, "wb")
    idwriter = csv.writer(idfile, delimiter=",")

    while True:
        try:
            inp = raw_input("Enter ID: ")
            if len(inp) > 9:
                inp = inp[:-1]
            num = int(inp)
            if num < 0: #num=="-1":
                break
            #num = num[8:11]
            found, name = idtoname(roster_file, num)
	    if found:
                #print "Converted " + str(num) + " to " + name
                print "Thank you, " + name + "(" + str(num) + ")"
                idwriter.writerow([name, datetime.time.strftime(datetime.datetime.now().time(), "%I:%M:%S")])
		idfile.flush()
            else:
                print "error: '" + str(num) + "' in not a valid id number" #"Could not get name for User " + str(num)
        except:
            print "error: '" + inp + "' is not a number"
    idfile.close()
    print "--- FINISHED ID FETCH ---"
    return filename


def findtimediffs(time_file):
    print "--- STARTING TIME DIFF ---"
    times = []
    queue = [[""]]
    gotname = False
    timefile = open(time_file, "r+b")
    timereader = csv.reader(timefile, delimiter=",")
    for lines in timereader:
        times.append(lines)
    timefile.seek(0, 2)
    timefile.write("\n")
    for line in times:
        for person in queue:
            if line[0] == person[0]:
                time1 = datetime.datetime.strptime(line[1], '%I:%M:%S')
                time2 = datetime.datetime.strptime(person[1], '%I:%M:%S')
                print line[0] + ": Got times " + str(time1.strftime("%I:%M:%S")) + " and " + str(time2.strftime("%I:%M:%S"))
                diff =  time1 - time2
                print line[0] + ": Got diff " + str(diff)
                timefile.write(str(line[0]) + "," + str(diff) + "\n")
                queue.remove(person)
                gotname = True
        if not gotname:
            print line[0] + ": Added to queue"
            queue.append(line)
    timefile.close()
    print "--- FINISHED TIME DIFF ---"

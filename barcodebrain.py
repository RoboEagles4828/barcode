import csv
import datetime

time = []
name = []


def idconvert(roster_file, time_file):
    print "--- STARTING ID CONVERSION ---"

    namefile = open(roster_file, "r")
    timefile = open(time_file, "r+b")

    namereader = csv.reader(namefile, delimiter=",")
    timereader = csv.reader(timefile, delimiter=",")

    for lines in timereader:
        time.append(lines)
    for lines in namereader:
        name.append(lines)

    timefile.seek(0)

    for line in time:
        for key in name:
            if line[0] == key[0]:
                print "Change " + line[0] + " to " + key[1]
                timefile.write(str(key[1]) + "," + str(line[1]) + "\n")
    namefile.close()
    timefile.close()
    print "--- FINISHED ID CONVERSION ---"


def getid():
    print "--- STARTING ID FETCH ---"
    filename = "attendance/attendance" + str(
        datetime.date.strftime(datetime.datetime.today().date(), "%m-%d-%y")) + ".csv"
    print "Log Name: " + filename

    idfile = open(filename, "wb")
    idwriter = csv.writer(idfile, delimiter=",")

    while True:
        num = raw_input("Enter ID: ")
        if num == "-1":
            break
        num = num[8:11]
        print "Thank you, User " + num
        idwriter.writerow([num, datetime.time.strftime(datetime.datetime.now().time(), "%I:%M:%S")])
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

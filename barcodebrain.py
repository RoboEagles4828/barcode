import csv
import datetime

time = []
name = []


def idconvert(roster_file, time_file):
    namefile = open(roster_file, "r")
    timefile = open(time_file, "r+b")

    namereader = csv.reader(namefile, delimiter=",")
    timereader = csv.reader(timefile, delimiter=",")

    for lines in timereader:
        time.append(lines)
    for lines in namereader:
        name.append(lines)

    print time
    print name

    timefile.seek(0)

    for line in time:
        for key in name:
            if line[0] == key[0]:
                timefile.write(str(key[1]) + "," + str(line[1]) + "\n")
    namefile.close()
    timefile.close()


def getid():
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
    return filename


def findtimediffs(time_file):
    times = []
    queue = [[""]]
    gotname = False
    timefile = open(time_file, "r+b")
    timereader = csv.reader(timefile, delimiter=",")
    for lines in timereader:
        times.append(lines)
    timefile.seek(0, 2)
    timefile.write("\n")
    print times
    for line in times:
        print queue
        print line
        for person in queue:
            print person[0]
            if line[0] == person[0]:
                diff = datetime.datetime.strptime(
                    line[1], '%I:%M:%S') - datetime.datetime.strptime(
                    person[1], '%I:%M:%S')
                print diff
                timefile.write(str(line[0]) + "," + str(diff) + "\n")
                queue.remove(person)
                gotname = True
        if not gotname:
            queue.append(line)
    timefile.close()
